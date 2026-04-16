from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact
)
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils import utils

from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
import os
import sys


class DataValidation:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_validation_config: DataValidationConfig,
    ):
        try:
            logging.info("Initializing DataValidation class.")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = utils.read_yaml_file(SCHEMA_FILE_PATH)
            logging.info(f"Schema loaded from: {SCHEMA_FILE_PATH}")
            logging.info(f"Schema Content: {self._schema_config}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            logging.info(f"Reading data from: {file_path}")
            df = pd.read_csv(file_path)
            logging.info(f"Data loaded successfully with shape: {df.shape}")
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            logging.info("Starting column validation.")

            schema_columns = self._schema_config["columns"]

            # Extract column names from schema
            if isinstance(schema_columns, list):
                if isinstance(schema_columns[0], dict):
                    expected_columns = [
                        list(column.keys())[0] for column in schema_columns
                    ]
                else:
                    expected_columns = schema_columns
            elif isinstance(schema_columns, dict):
                expected_columns = list(schema_columns.keys())
            else:
                raise ValueError("Invalid schema format for 'columns'.")

            logging.info(f"Expected Columns: {expected_columns}")
            logging.info(f"Actual Columns: {list(dataframe.columns)}")

            missing_columns = list(
                set(expected_columns) - set(dataframe.columns)
            )
            extra_columns = list(
                set(dataframe.columns) - set(expected_columns)
            )

            if missing_columns:
                logging.error(f"Missing columns: {missing_columns}")
                return False

            if extra_columns:
                logging.warning(f"Extra columns detected: {extra_columns}")

            logging.info("Column validation passed successfully.")
            return True

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(
        self,
        base_df: pd.DataFrame,
        current_df: pd.DataFrame,
        threshold: float = 0.05,
    ) -> bool:
        try:
            logging.info("Starting dataset drift detection using KS test.")
            status = True
            report = {}

            numerical_columns = base_df.select_dtypes(
                include=[np.number]
            ).columns

            for column in numerical_columns:
                logging.info(f"Analyzing drift for column: {column}")

                d1 = base_df[column].dropna()
                d2 = current_df[column].dropna()

                if len(d1) == 0 or len(d2) == 0:
                    logging.warning(
                        f"Skipping column '{column}' due to insufficient data."
                    )
                    continue

                ks_test = ks_2samp(d1, d2)
                drift_detected = ks_test.pvalue < threshold

                if drift_detected:
                    status = False

                report[column] = {
                    "p_value": float(ks_test.pvalue),
                    "drift_status": drift_detected,
                }

            drift_report_file_path = (
                self.data_validation_config.drift_report_file_path
            )
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)

            utils.write_yaml_file(
                file_path=drift_report_file_path,
                content=report,
            )

            logging.info(f"Drift report saved at: {drift_report_file_path}")
            logging.info(f"Overall drift status: {status}")

            return status

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logging.info("Starting data validation process.")
            error_message = ""

            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = self.read_data(train_file_path)
            test_df = self.read_data(test_file_path)

            # Validate columns
            if not self.validate_columns(train_df):
                error_message += (
                    "Train dataframe does not contain all required columns.\n"
                )

            if not self.validate_columns(test_df):
                error_message += (
                    "Test dataframe does not contain all required columns.\n"
                )

            if error_message:
                logging.error(error_message)
                raise Exception(error_message)

            # Detect dataset drift
            drift_status = self.detect_dataset_drift(
                base_df=train_df,
                current_df=test_df,
            )

            validation_status = drift_status

            # Create directories
            os.makedirs(
                os.path.dirname(
                    self.data_validation_config.valid_train_file_path
                ),
                exist_ok=True,
            )

            # Save validated datasets
            train_df.to_csv(
                self.data_validation_config.valid_train_file_path,
                index=False,
                header=True,
            )

            test_df.to_csv(
                self.data_validation_config.valid_test_file_path,
                index=False,
                header=True,
            )

            logging.info(
                "Validated train and test datasets saved successfully."
            )

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            logging.info("Data validation artifact created successfully.")
            logging.info("Data validation process completed.")

            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)