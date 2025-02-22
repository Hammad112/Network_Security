from NetworkSecurity.logging.logger import logging
from NetworkSecurity.exception.exception import NetworkSecurityException

## Data Drift 
import pandas as pd
import sys,os
import yaml

import pickle
#import dill
import numpy as np

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


