from NetworkSecurity.logging.logger import logging
from NetworkSecurity.exception.exception import NetworkSecurityException

## Data Drift 
import pandas as pd
import sys,os
import yaml

import pickle
#import dill
import numpy as np


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path,'rb') as read_yaml:
            return yaml.safe_load(read_yaml)
    
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e

def write_yaml(file_path: str, content: object, replace: bool = False) -> None:
    try:
        # Remove the file if replace=True and it exists
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write YAML content
        with open(file_path, "w") as file:
            yaml.dump(content, file)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
        