from NetworkSecurity.logging.logger import logging
from NetworkSecurity.exception.exception import NetworkSecurityException

## Data Drift 
import pandas as pd
import sys,os
import yaml

import pickle
#import dill
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


## Read Yaml File
def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path,'rb') as read_yaml:
            return yaml.safe_load(read_yaml)
    
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e


## Write Yaml FIle

def write_yaml(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

 
## Save Numpy Array 
def save_numpy_array(file_path:str, array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb')as file_obj:
            np.save(file_obj,array)
    
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e


## Loading Numpy Array
def load_numpy_array(file_path: str) -> np.array:
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj, allow_pickle=True)  
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


## SavePickel File
def save_pickle(file_path:str ,obj : object) -> None:
    try:
        logging.info("Entered the save model method of MainUtils class")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Exited the save object method od Main utils class")
    
    except Exception as e:
        raise NetworkSecurityException (e,sys) from e


## Loading Pickle
def load_pickle(file_path:str,) ->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file :{file_path} doesnot exists")
        
        with open(file_path,'rb') as file_obj:
            print(file_obj)
            return pickle.load(file_obj)

    except Exception as e:
        raise NetworkSecurityException (e,sys) from e
    

def evaluate_model(x_train,y_train,x_test,y_test,models,params):
    try:
        report = {}
         
        for i in range(len(list(models))):

            model = list(models.values())[i]
            model_params = params[list(models.keys())[i]]


            gs = GridSearchCV(model, model_params, cv=3 , error_score="raise")
            gs.fit(x_train, y_train)

            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)

            y_train_pred = model.predict(x_train)

            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report        
    except Exception as e:
        raise NetworkSecurityException(e,sys)