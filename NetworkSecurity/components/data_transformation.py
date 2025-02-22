import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
import sys,os

## Logging And Exception
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

## Target Column && KNN IMPUTER PARAMS
from NetworkSecurity.constant.training_pipeline import TARGET_NAME,DATA_TRANSFORMATION_IMPUTER_PARAMS

## configuration file for data Config
from NetworkSecurity.entity.config_entity import DataTransformationConfig
from NetworkSecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact

## save pickle and 
from NetworkSecurity.utils.main_utils.utils import save_numpy_array,save_pickle


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact, data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact

            self.data_transformation_config:DataTransformationConfig=data_transformation_config

        except Exception as e:
            raise NetworkSecurityException (e,sys)


        ## Reading CSVs
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        
        except Exception as e:
            raise NetworkSecurityException (e,sys)

    ## KNN impuuter
    def get_data_tranformed_object(cls) -> Pipeline:
        logging.info("Entered get_data_tranformed_object ")
        
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)  
            processor: Pipeline = Pipeline([('imputer', imputer)])  # Correct
            
            return processor

        except Exception as e:
            raise NetworkSecurityException(e,sys)



    def intiate_data_transformation(self) ->DataTransformationArtifact:
        try:
            logging.info("Starting Data Transformation")
            ## Reading Data sets
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            ## Train DataFrame 
            input_feature_train_df=train_df.drop(columns=[TARGET_NAME],axis=1)
            target_feature_train=train_df[TARGET_NAME]
            ## Replacing -1 to 1 
            target_feature_train=target_feature_train.replace(-1,0)

            ## Test DataFrame
            input_feature_test_df=test_df.drop(columns=[TARGET_NAME],axis=1)
            target_feature_test=test_df[TARGET_NAME]
            ## Replacing -1 to 1 
            target_feature_test=target_feature_test.replace(-1,0)

            
            ## Applying KNN Imputer To Handle Missing Value
            preprocessor=self.get_data_tranformed_object()
            processor_obj=preprocessor.fit(input_feature_train_df)
           
            transformed_input_train_feature=processor_obj.transform(input_feature_train_df)
            transformed_input_test_feature=processor_obj.transform(input_feature_test_df)


            ## To Numpy Array 
            train_array=np.c_[transformed_input_train_feature,np.array(target_feature_train)]
            test_array=np.c_[transformed_input_test_feature,np.array(target_feature_test)]
            
            ## Saving Numpy Array
            save_numpy_array(self.data_transformation_config.transformed_train_file_path,array=train_array,)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path,array=test_array,)
            save_pickle(self.data_transformation_config.transformed_object_file_path,processor_obj,)

            ## Preparing Artifacts
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_object_file_path
            )

            return data_transformation_artifact




        except Exception as e:
            raise NetworkSecurityException(e,sys)

    