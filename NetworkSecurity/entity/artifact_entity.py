from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    train_filepath:str
    test_filepath:str


@dataclass
class DataValidationArtifact:
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    data_drift_file_path:str
