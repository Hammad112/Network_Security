import os
import sys
import mlflow
import dagshub
import mlflow.pyfunc
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

## Import Custom Modules
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import ModelTrainerConfig
from NetworkSecurity.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact
from NetworkSecurity.utils.main_utils.utils import save_pickle, load_pickle, load_numpy_array, evaluate_model
from NetworkSecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from NetworkSecurity.utils.ml_utils.model.estimator import NetworkModel

## Initialize Dagshub for MLflow Tracking
dagshub.init(repo_owner="Hammad112", repo_name="Network_Security", mlflow=True)

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    ## MLflow Model Tracking
    def track_mlflow(self, model, model_name, model_score):
        with mlflow.start_run():
            mlflow.log_params({"best_model_name": model_name})
            mlflow.log_metrics({
                "f1_score": model_score.f1_score,
                "precision_score": model_score.precision_score,
                "recall_score": model_score.recall_score
            })
            mlflow.sklearn.log_model(model, "Model")  # Corrected logging

    ## Train and Select the Best Model
    def train_model(self, x_train, y_train, x_test, y_test):
        try:
            models = {
                "Decision Tree": DecisionTreeClassifier(),
                "Random Forest": RandomForestClassifier(),
                "Logistic Regression": LogisticRegression()
            }

            params = {
                "Decision Tree": {"criterion": ["gini", "entropy"]},
                "Random Forest": {"criterion": ["gini", "entropy"]},
                "Logistic Regression": {"penalty": ["l2"]}
            }

            ## Evaluate Models
            model_report = evaluate_model(x_train, y_train, x_test, y_test, models, params)
            print(model_report)

            ## Get Best Model
            best_model_name = max(model_report, key=model_report.get)  # Get model with max score
            best_model = models[best_model_name]

            ## Train Model on Full Training Data
            best_model.fit(x_train, y_train)

            ## Evaluate on Train and Test Set
            y_train_pred = best_model.predict(x_train)
            y_test_pred = best_model.predict(x_test)

            train_model_score = get_classification_score(y_train, y_train_pred)
            test_model_score = get_classification_score(y_test, y_test_pred)

            logging.info(f"Best Model Found: {best_model_name}")

            ## Track with MLflow
            self.track_mlflow(best_model, best_model_name, train_model_score)
            self.track_mlflow(best_model, best_model_name, test_model_score)

            ## Save Model
            preprocessor = load_pickle(self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)

            ## Wrap Model with Preprocessor
            network_model = NetworkModel(preprocessor=preprocessor, model=best_model)

            ## Save Final Model
            save_pickle(self.model_trainer_config.trained_model_file_path, network_model)

            ## Ensure Final Model Directory Exists
            final_model_dir = "final_model"
            os.makedirs(final_model_dir, exist_ok=True)
            save_pickle(os.path.join(final_model_dir, "model.pkl"), best_model)

            logging.info(f"Model Saved at: {self.model_trainer_config.trained_model_file_path}")

            return ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=train_model_score,
                test_metric_artifact=test_model_score
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            ## Load Train & Test Data
            train_array = load_numpy_array(self.data_transformation_artifact.transformed_train_file_path)
            test_array = load_numpy_array(self.data_transformation_artifact.transformed_test_file_path)

            ## Split Data
            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            ## Train Model
            return self.train_model(x_train, y_train, x_test, y_test)

        except Exception as e:
            raise NetworkSecurityException(e, sys) from e
