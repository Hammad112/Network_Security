import os
import sys
import numpy as np
import pandas as pd


## 01:Data Ingestion

### Defining Some Data Ingestion Constants 
TARGET_NAME="Result"
PIPELINE_NAME:str='NetworkSecurity'
ARTIFACT_DIR:str='Artifacts'
FILE_NAME:str="NetworkData.csv"
TRAIN_FILENAME:str="train.csv"
TEST_FILENAME:str="test.csv"
SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")

## Data Ingestion Constant
DATA_INGESTION_COLLECTION_NAME:str="PhishingData"
DATA_INGESTION_DATABASE_NAME:str="NetworkData"
DATA_INGESTION_DIR_PATH:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2


## 02: Data Validation
DATA_VALIDATION_DIR_PATH:str="data_validation"
VALID_VALIDATION_DATA_DIR:str='Validated'
INVALID_VALIDATION_DATA_DIR:str='Invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR:str='drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE:str='drift_report.yaml'

## Data Transformation
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str='transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str='transformed_object'
DATA_TRANSFORMATION_DIR_NAME='data_transformation'
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

## KNN Imputer to Replace NAN Value
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    'missing_values': np.nan,
    'n_neighbors': 3,  # Correct spelling
    'weights': 'uniform',
}
DATA_TRANSFORMATION_TRAIN_FILE_PATH :str ='train.npy'
DATA_TRANSFORMATION_TEST_FILE_PATH : str ='test.npy'

## MODEL TRAINER CONSTANATS
MODEL_TRAINER_DIR_NAME: str ='Model Trainer'
MODEL_TRAINER_TRAINED_MODEL_DIR: str='Trained Model'
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD : float =0.05
MODEL_TRAINER_EXPECTED_SCORE:float =0.6

SAVE_MODEL_DIR=os.path.join("saved_model")
SAVED_MODEL_NAME:str ='model.pkl'
