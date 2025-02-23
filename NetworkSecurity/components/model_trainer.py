import sys,os

## Logging And Exception
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging

## configuration file for data Config
from NetworkSecurity.entity.config_entity import ModelTrainerConfig
from NetworkSecurity.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact

from NetworkSecurity.utils.main_utils.utils import save_pickle,load_pickle,load_numpy_array,evaluate_model
from NetworkSecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier
)
import mlflow
import dagshub
dagshub.init(repo_owner='Hammad112', repo_name='Network_Security', mlflow=True)





class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException (e,sys) from e

    ## MLFLOW TRACKING
    def track_mlflow(self,best_model_name,best_model_score):
        with mlflow.start_run():
            f1_score=best_model_score.f1_score
            precision_score=best_model_score.precision_score
            recall_score=best_model_score.recall_score

            mlflow.log_params({"best_model_name":best_model_name,"best_model_score":best_model_score})
            mlflow.log_metrics({"f1_score":f1_score,"precision_score":precision_score,"recall_score":recall_score})

            mlflow.sklearn.log_model(best_model_name,"Model")
            
    ## Creating model Function
    def train_model(self,x_train,y_train,x_test,y_test):
        try:
            models = {
                    "Decision Tree": DecisionTreeClassifier(),
                    "Random Forest": RandomForestClassifier(),
                    'Logistic Regression': LogisticRegression(),
              
                }

            params = {
                    "Decision Tree": { "criterion": ["gini", "entropy"] },
                    "Random Forest": { "criterion": ["gini", "entropy"] },
                    "Logistic Regression": { "penalty": [ "l2"] },
                }

           

            ## Evaluating 
            model_report:dict=evaluate_model(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,models=models,params=params)
            print(model_report)

            ## Selecting Model
            best_model_score=max(sorted(model_report.values()))

            ## Getting Best Model Name 
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
             ]

            best_model=models[best_model_name]

            y_train_pred=best_model.predict(x_train)
            
            train_model_score=get_classification_score(y_actual=y_train,y_pred=y_train_pred)


            logging.info(f"Best Model Found on both training and testing dataset")
            
            ## Track Model with MLFLOW
            self.track_mlflow(best_model_name,train_model_score)

            ## Test Set

            logging.info(f"Best Model Found on both training and testing dataset")

            y_train_pred=best_model.predict(x_train)

            train_model_score=get_classification_score(y_actual=y_train,y_pred=y_train_pred)
            ## Track Model

            y_test_pred=best_model.predict(x_test)

            test_model_score=get_classification_score(y_actual=y_test,y_pred=y_test_pred)

            ##Tracking Test Set with MLFLOW
            self.track_mlflow(best_model_name,test_model_score)

            ## Load model
            preprocessor=load_pickle(self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)


            network_model=NetworkModel(
                preprocessor=preprocessor,
                model=best_model
              )

            save_pickle(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=network_model
              )

            save_pickle('/final_model/model.pkl',best_model)


            model_trainer_artifact=ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=train_model_score,
                test_metric_artifact=test_model_score
              )

            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
                
            return model_trainer_artifact
                


        except Exception as e:
            raise NetworkSecurityException (e,sys) from e

        
    def intiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            ## Loading train and test file path
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path


            ## Loading Train and Test Numpy Array
            train_array=load_numpy_array(train_file_path)
            test_array=load_numpy_array(test_file_path)


            ## Splitting Data
            x_train, y_train, x_test, y_test=(
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
               )


            ## Creating Model
            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException (e,sys) from e