from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

## configuration file for data ingestion Config
from NetworkSecurity.entity.config_entity import DataValidationConfig
from NetworkSecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

## Data Drift 
from scipy.stats import ks_2samp
import pandas as pd
import sys,os

from NetworkSecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from NetworkSecurity.utils.main_utils.utils import read_yaml_file,write_yaml

class DataValidation:
    def __init__(
        self,
        data_validation_config: DataValidationConfig,
        data_ingestion_artifact: DataIngestionArtifact
    ):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

     
    @staticmethod
    def read_data(file_path) ->pd.DataFrame:
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise NetworkSecurityException (e,sys)

    ## Comparing Actual dataset Columns with splitted dataset columns
    def Validate_Columns(self,dataframe:pd.DataFrame)->bool:
        try:
            numer_of_columns=len(self._schema_config)
            logging.info(f"Required number of columns - {numer_of_columns}")
            logging.info(f"Dataframe in columns - {len(dataframe.columns)}")
            if len(dataframe.columns)==numer_of_columns:
                return True
            else:
                return False
    
        except Exception as e:
            raise NetworkSecurityException (e,sys)

    ## Validate Numerical Column
    def Validate_Numerical_Columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            numerical_columns = dataframe.select_dtypes(include=['number']).columns
            if len(numerical_columns) > 0:
                logging.info("Numerical columns exist in the dataframe.")
                return True
            else:
                logging.info("No numerical columns found in the dataframe.")
                return False

        except Exception as e:
            raise NetworkSecurityException(e,sys)


    ## Data Drift
    def Detect_Drift(self, base_df , current_df, threshold=0.05) -> bool:
        try:
            status=True
            report={}
            for columns in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_smaple_dit_same_not=ks_2samp(d1,d2)
                if threshold <=is_smaple_dit_same_not.pvalue:
                    isfound=False
                else:
                    isfound=False
                    status=False
                
                report.update({
                    column:{
                        'pvalue':float(is_smaple_dit_same_not.pvalue),
                        'drift_status':isfound
                    }
                })
                drif_report_file_path=self.data_validation_config.data_drift_file_path
                os.makedirs(drif_report_file_path,exist_ok=True)
                write_yaml(file_path=drif_report_file_path,content=report)
                
       
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    


    def intiate_data_validation(self) ->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.train_filepath
            test_file_path=self.data_ingestion_artifact.test_filepath

            ## Read Test and Train 
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)

            ## Validate Number of Columns
            ## Train
            status_train=self.Validate_Columns(dataframe=train_dataframe)
            
            if not status_train:
                return f' Train dataframe does not contain all columns'

            ## Test
            
            status_test=self.Validate_Columns(dataframe=test_dataframe)
            
            if not status_test:
                return f'{error_message} Train dataframe does not contain all columns'

   
            ## Numerical Columns Exists or not
            num_col_train=self.Validate_Numerical_Columns(dataframe=train_dataframe)
            if not num_col_train:
                return f'{error_message} Train dataframe does not contain Numerical columns'

           

            num_col_test=self.Validate_Numerical_Columns(dataframe=test_dataframe)
            if not num_col_test:
                return f'Train dataframe  contain Nuumerical columns'

            ## Data Drift
            status=self.Detect_Drift(base_df=train_dataframe,current_df=test_dataframe)
            os_path=os.path.dirname(self.DataValidationConfig.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,index=False,header=True
            )


            data_validation_artifact=DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_filepath,
                valid_test_file_path=self.data_ingestion_artifact.test_filepath,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drif_report_file_path=self.data_validation_config.drif_report_file_path

            )




        except Exception as e:
            raise NetworkSecurityException(e,sys)