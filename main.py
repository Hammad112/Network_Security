from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig
from NetworkSecurity.components.data_validation import DataValidation



from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
import sys

if __name__=='__main__':
    try:
        ## Training Pipeline Configuration
        trainingpipelineconfig=TrainingPipelineConfig()

        ## Data Ingestion Configuration
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info('Intitate data ingestion')
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Ingestion Completed")

        ## Data Validation
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(data_ingestion_artifact=dataingestionartifact,data_validation_config=data_validation_config)
        logging.info("Intiating Data Validation ")
        data_validation_Artifact=data_validation.intiate_data_validation()
        logging.info("Data Validation Completed ")

        ## Data Transformation


    except Exception as e:
        raise NetworkSecurityException(e,sys)
