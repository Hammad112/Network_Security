import os
import sys
import numpy as np
import pandas as pd

### Defining Some Constants
TARGET_NAME="Result"
PIPELINE_NAME:str='NetworkSecurity'
ARTIFACT_DIR:str='Artifacts'
FILE_NAME:str="NetworkData.csv"

TRAIN_FILENAME:str="train.csv"
TEST_FILENAME:str="test.csv"



## Data Ingestion Constant
DATA_INGESTION_COLLECTION_NAME:str="PhishingData"
DATA_INGESTION_DATABASE_NAME:str="NetworkData"
DATA_INGESTION_DIR_PATH:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float=0.2