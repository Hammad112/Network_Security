from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

## configuration file for data ingestion Config
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact

import os
import sys
import numpy as np
import pymongo
import pandas as pd
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

## loading Mongo db url
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

## Read from Mongo DB Data
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
            
        except:
            raise NetworkSecurityException(e,sys)


    ## Reading Data And Converting into Data Frame
    def export_data_as_DF_MongoDB(self):
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find()))
            

            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"],inplace=True)
            
            df.replace({"na":np.nan},inplace=True)
            return df

        except Exception as e:
            raise NetworkSecurityException(e,sys)

        
    ## Storing dataframe to Feature Store 
    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:

            feature_store_file_path = self.data_ingestion_config.feature_store_path
            ## Creating Folder
            dir_path = os.path.dirname(feature_store_file_path)
            print(dir_path)
            os.makedirs(dir_path, exist_ok=True)

            ## Storing Data
            dataframe.to_csv(feature_store_file_path, index=False, header=True)  
            return dataframe 

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    ## Train Test Split 
    def train_test_split_df(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on Data Frame")
            logging.info(
                "Exited Split data as Train sets and test sets method of Data_Ingestion class"
            )
            dir_path=os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Exporting train and test file path")
            
            train_set.to_csv(
                self.data_ingestion_config.train_file_path,index=False,header=True

            )

            test_set.to_csv(
                self.data_ingestion_config.test_file_path,index=False,header=True
            )
            logging.info(f"Exported Train and Test File Path")


        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_data_as_DF_MongoDB()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.train_test_split_df(dataframe)
            dataingestionartifact=DataIngestionArtifact(
                trained_filepath=self.data_ingestion_config.train_file_path,
                test_filepath=self.data_ingestion_config.test_file_path
            )
            return dataingestionartifact


            
        except Exception as e:
            raise NetworkSecurityException(e,sys)



