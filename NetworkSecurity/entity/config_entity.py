from datetime import datetime
import os
from NetworkSecurity.constant import training_pipeline


class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y")
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifacts_name=training_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifacts_name,timestamp)
        self.timestamp: str=timestamp


class DataIngestionConfig:
    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        ## Data Ingestion Directory Path
        self.data_ingestion_dir : str=os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_PATH
        )
        ## Feature Store Path
        self.feature_store_path : str=os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE,
            training_pipeline.FILE_NAME

        )
        ## Train File Path
        self.train_file_path : str=os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_DIR_PATH,
            training_pipeline.TRAIN_FILENAME
        )
        ## Test File Path
        self.test_file_path : str=os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_DIR_PATH,
            training_pipeline.TEST_FILENAME
        )
        ## Data Ingestion Collection Name
        self.collection_name : str=training_pipeline.DATA_INGESTION_COLLECTION_NAME
        ## Data Ingestion Database Name
        self.database_name : str=training_pipeline.DATA_INGESTION_DATABASE_NAME
        ## Data Ingestion Train Test Split Ratio
        self.train_test_split_ratio : float=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO