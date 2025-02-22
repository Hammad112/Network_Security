from dataclasses import dataclass

## DAta Ingestion Class
@dataclass
class DataIngestionArtifact:
    train_filepath:str
    test_filepath:str

## Data Validation Class
@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    data_drift_file_path:str


## Data Transformation Class
@dataclass
class DataTransformationArtifact:
    transformed_object_file_path:str 
    transformed_train_file_path:str
    transformed_test_file_path:str