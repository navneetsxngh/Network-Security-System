from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys


if __name__ == '__main__':
    try:
        logging.info("Enter the Try Block")
        trainig_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(trainig_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)

        logging.info("Initiate data Ingestion")
        artifact = data_ingestion.initiate_data_ingestion()
        print(artifact)
    
    except Exception as e:
        raise NetworkSecurityException(e, sys)
