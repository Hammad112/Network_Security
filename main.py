from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.components.data_transformation import DataTransformation
from NetworkSecurity.components.model_trainer import ModelTrainer


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
        data_validation_artifact=data_validation.intiate_data_validation()
        logging.info("Data Validation Completed ")

        ## Data Transformation
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=data_transformation_config)
        logging.info("Intiating Data Transformation")
        data_transformation_artifact=data_transformation.intiate_data_transformation()
        logging.info("Data Transformation Completed")
  

        ## Model Training
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        logging.info("Intiating Data Transformation")
        model_trainer_artifact=model_trainer.intiate_model_trainer()
        logging.info("Data Transformation Completed")
        print(model_trainer_artifact)



    except Exception as e:
        raise NetworkSecurityException(e,sys)
