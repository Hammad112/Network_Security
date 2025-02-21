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