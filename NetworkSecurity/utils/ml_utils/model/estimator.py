import sys,os

## Logging And Exception
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

## importing Constants
from NetworkSecurity.constant.training_pipeline import SAVED_MODEL_NAME,SAVE_MODEL_DIR


class NetworkModel:
    ## intialization
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model

        except Exception as e:
            raise NetworkSecurityException (e,sys)

    
    def predict(self,x):
        try:
            x_transformed=self.preprocessor.transform()
            y_hat=self.model.predict(x_transformed)
            return y_hat

        except Exception as e:
            raise NetworkSecurityException (e,sys)
    