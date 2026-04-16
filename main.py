from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
# from networksecurity.components.data_transformation import DataTransformation
# from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    TrainingPipelineConfig,
)
# from networksecurity.entity.config_entity import (
#     DataTransformationConfig,
#     ModelTrainerConfig
# )

import sys


def run_training_pipeline():
    """
    Executes the Network Security Training Pipeline.
    """
    try:
        logging.info("=" * 80)
        logging.info("🚀 NETWORK SECURITY TRAINING PIPELINE STARTED")
        logging.info("=" * 80)

        # Initialize Training Pipeline Configuration
        training_pipeline_config = TrainingPipelineConfig()
        logging.info("TrainingPipelineConfig initialized successfully.")

        # ==============================
        # DATA INGESTION STAGE
        # ==============================
        logging.info("Starting Data Ingestion Stage.")

        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)

        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")

        print("\nData Ingestion Artifact:")
        print(data_ingestion_artifact)

        logging.info("Data Ingestion Stage Completed.")
        logging.info("-" * 80)

        # ==============================
        # DATA VALIDATION STAGE
        # ==============================
        logging.info("Starting Data Validation Stage.")

        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(
            data_ingestion_artifact, data_validation_config
        )

        data_validation_artifact = (
            data_validation.initiate_data_validation()
        )
        logging.info(f"Data Validation Artifact: {data_validation_artifact}")

        print("\nData Validation Artifact:")
        print(data_validation_artifact)

        logging.info("Data Validation Stage Completed.")
        logging.info("-" * 80)

        # ==============================
        # DATA TRANSFORMATION STAGE
        # ==============================
        # logging.info("Starting Data Transformation Stage.")
        # data_transformation_config = DataTransformationConfig(
        #     training_pipeline_config
        # )
        # data_transformation = DataTransformation(
        #     data_validation_artifact,
        #     data_transformation_config
        # )
        # data_transformation_artifact = (
        #     data_transformation.initiate_data_transformation()
        # )
        # logging.info(
        #     f"Data Transformation Artifact: {data_transformation_artifact}"
        # )
        # print("\nData Transformation Artifact:")
        # print(data_transformation_artifact)
        # logging.info("Data Transformation Stage Completed.")
        # logging.info("-" * 80)

        # ==============================
        # MODEL TRAINING STAGE
        # ==============================
        # logging.info("Starting Model Training Stage.")
        # model_trainer_config = ModelTrainerConfig(
        #     training_pipeline_config
        # )
        # model_trainer = ModelTrainer(
        #     model_trainer_config=model_trainer_config,
        #     data_transformation_artifact=data_transformation_artifact
        # )
        # model_trainer_artifact = (
        #     model_trainer.initiate_model_trainer()
        # )
        # logging.info(
        #     f"Model Trainer Artifact: {model_trainer_artifact}"
        # )
        # logging.info("Model Training Stage Completed.")

        logging.info("=" * 80)
        logging.info("✅ TRAINING PIPELINE COMPLETED SUCCESSFULLY")
        logging.info("=" * 80)

    except Exception as e:
        logging.exception("An error occurred during pipeline execution.")
        raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    run_training_pipeline()