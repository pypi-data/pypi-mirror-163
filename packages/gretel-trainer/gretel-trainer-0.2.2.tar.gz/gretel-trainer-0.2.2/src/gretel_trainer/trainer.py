"""Main Trainer Module"""

import json
import logging
import os.path

import pandas as pd
from gretel_client import configure_session
from gretel_client.projects import create_or_get_unique_project
from gretel_synthetics.utils.header_clusters import cluster

from gretel_trainer import runner, strategy
from gretel_trainer.models import _BaseConfig, GretelLSTM

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

DEFAULT_PROJECT = "trainer"
DEFAULT_CACHE = f"{DEFAULT_PROJECT}-runner.json"


class Trainer:
    """Automated model training and synthetic data generation tool

    Args:
        project_name (str, optional): Gretel project name. Defaults to "trainer".
        model_config (_BaseConfig, optional): Options include GretelLSTM(), GretelCTGAN(). Defaults to GretelLSTM().
        cache_file (str, optional): Select a path to save or load the cache file. Default is `[project_name]-runner.json`. 
        overwrite (bool, optional): Overwrite previous progress. Defaults to True.
    """

    def __init__(
        self,
        project_name: str = "trainer",
        model_type: _BaseConfig = GretelLSTM(),
        cache_file: str = None,
        overwrite: bool = True,
    ):
        configure_session(api_key="prompt", cache="yes", validate=True)

        self.df = None
        self.dataset_path = None
        self.run = None
        self.project_name = project_name
        self.project = create_or_get_unique_project(name=project_name)
        self.overwrite = overwrite
        self.cache_file = self._get_cache_file(cache_file)
        self.model_type = model_type

        if self.overwrite:
            logger.debug(json.dumps(self.model_type.config, indent=2))

    @classmethod
    def load(
        cls, cache_file: str = DEFAULT_CACHE, project_name: str = DEFAULT_PROJECT
    ) -> runner.StrategyRunner:
        """Load an existing project from a cache.

        Args:
            cache_file (str, optional): Valid file path to load the cache file from. Defaults to `[project-name]-runner.json` 

        Returns:
            Trainer: returns an initialized StrategyRunner class.
        """
        project = create_or_get_unique_project(name=project_name)
        model = cls(cache_file=cache_file, project_name=project_name, overwrite=False)

        if not os.path.exists(cache_file):
            raise ValueError(
                f"Unable to find `{cache_file}`. Please specify a valid cache_file."
            )

        model.run = model._initialize_run(df=None, overwrite=model.overwrite)
        return model

    def train(
        self, dataset_path: str, round_decimals: int = 4, seed_fields: list = None
    ):
        """Train a model on the dataset

        Args:
            dataset_path (str): Path or URL to CSV
            round_decimals (int, optional): Round decimals in CSV as preprocessing step. Defaults to `4`.
            seed_fields (list, optional): List fields that can be used for conditional generation.
        """
        self.dataset_path = dataset_path
        self.df = self._preprocess_data(
            dataset_path=dataset_path, round_decimals=round_decimals
        )
        self.run = self._initialize_run(
            df=self.df, overwrite=self.overwrite, seed_fields=seed_fields
        )
        self.run.train_all_partitions()

    def generate(
        self, num_records: int = 500, seed_df: pd.DataFrame = None
    ) -> pd.DataFrame:
        """Generate synthetic data

        Args:
            num_records (int, optional): Number of records to generate from model. Defaults to 500.
            seed_df (pd.DataFrame, optional): Pandas DataFrame of values to seed the model with. Defaults to None.

        Returns:
            pd.DataFrame: Synthetic data.
        """
        self.run.generate_data(
            num_records=num_records if seed_df is None else None,
            max_invalid=None,
            clear_cache=True,
            seed_df=seed_df,
        )
        return self.run.get_synthetic_data()

    def get_sqs_score(self) -> int:
        """Return the average SQS synthetic data quality score.

        Requires the model has been trained.
        """
        scores = [
            sqs["synthetic_data_quality_score"]["score"]
            for sqs in self.run.get_sqs_information
        ]
        return int(sum(scores) / len(scores))

    def _preprocess_data(
        self, dataset_path: str, round_decimals: int = 4
    ) -> pd.DataFrame:
        """Preprocess input data"""
        tmp = pd.read_csv(dataset_path, low_memory=False)
        tmp = tmp.round(round_decimals)
        return tmp

    def _get_cache_file(self, cache_file: str) -> str:
        """Select a path to store the runtime cache to initialize a model"""
        if cache_file is None:
            cache_file = f"{self.project_name}-runner.json"

        if os.path.exists(cache_file):
            if self.overwrite:
                logger.warning(f"Overwriting existing run cache: {cache_file}.")
            else:
                logger.info(f"Using existing run cache: {cache_file}.")
        else:
            logger.info(f"Creating new run cache: {cache_file}.")
        return cache_file

    def _initialize_run(
        self, df: pd.DataFrame = None, overwrite: bool = True, seed_fields: list = None
    ) -> runner.StrategyRunner:
        """Create training jobs"""
        constraints = None
        if df is None:
            df = pd.DataFrame()

        if not df.empty:
            header_clusters = cluster(
                df,
                maxsize=self.model_type.max_header_clusters,
                header_prefix=seed_fields,
                plot=False,
            )
            logger.info(
                f"Header clustering created {len(header_clusters)} cluster(s) "
                f"of length(s) {[len(x) for x in header_clusters]}"
            )

            constraints = strategy.PartitionConstraints(
                header_clusters=header_clusters,
                max_row_count=self.model_type.max_rows,
                seed_headers=seed_fields,
            )

        run = runner.StrategyRunner(
            strategy_id=f"{self.project_name}",
            df=self.df,
            cache_file=self.cache_file,
            cache_overwrite=overwrite,
            model_config=self.model_type.config,
            partition_constraints=constraints,
            project=self.project,
        )
        return run
