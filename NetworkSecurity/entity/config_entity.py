from datetime import datetime
import os
from NetworkSecurity.constant import training_pipeline

## Data Ingestion 01
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

## Data Validation
class DataValidationConfig:
    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        ## Data Validation Directory Path
        self.data_validation_dir : str=os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIR_PATH
        )
        ## Valid Validation Data Directory
        self.valid_validation_data_dir : str=os.path.join(
            self.data_validation_dir,
            training_pipeline.VALID_VALIDATION_DATA_DIR
        )
        ## Invalid Validation Data Directory
        self.invalid_validation_data_dir : str=os.path.join(
            self.data_validation_dir,
            training_pipeline.INVALID_VALIDATION_DATA_DIR
        )
        ## Valid train file path
        self.valid_train_file_path :str=os.path.join(
            self.valid_validation_data_dir,
            training_pipeline.TRAIN_FILENAME
        )

        ## Valid test file path
        self.valid_test_file_path :str=os.path.join(
            self.valid_validation_data_dir,
            training_pipeline.TEST_FILENAME
        )

        ## invalid train file path
        self.invalid_train_file_path :str=os.path.join(
            self.invalid_validation_data_dir,
            training_pipeline.TRAIN_FILENAME
        )

        ## Invalid test file path
        self.invalid_test_file_path :str=os.path.join(
            self.invalid_validation_data_dir,
            training_pipeline.TEST_FILENAME
        )

        ## Data Validation Drift Report File
        self.data_drift_file_path : str=os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE
        )
