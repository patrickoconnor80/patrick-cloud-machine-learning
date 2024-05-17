from ray import serve

import numpy as np

from sklearn.datasets import load_iris
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import mean_squared_error

import mlflow
from mlflow.models import infer_signature
from ray.air.integrations.mlflow import setup_mlflow

TRACKING_URL = "https://kubernetes.patrick-cloud.com/mlflow/"
EXPERIMENT_NAME = "iris_gradient_boost_classifier_experiment"
MODEL_NAME = "iris_gradient_boost_classifier_model"

def train_gboost():

    # Set up Mlflow
    mlflow.set_tracking_uri(TRACKING_URL)
    mlflow.set_experiment(EXPERIMENT_NAME)
    mlflow.autolog()
    setup_mlflow(
        tracking_uri = TRACKING_URL,
        experiment_name = EXPERIMENT_NAME,
        create_experiment_if_not_exists = True
    )

    model = GradientBoostingClassifier()

    iris_dataset = load_iris()
    data, target, target_names = (
        iris_dataset["data"],
        iris_dataset["target"],
        iris_dataset["target_names"],
    )

    np.random.shuffle(data), np.random.shuffle(target)
    train_x, train_y = data[:100], target[:100]
    val_x, val_y = data[100:], target[100:]

    model.fit(train_x, train_y)
    mlflow.log_metric("MSE", mean_squared_error(model.predict(val_x), val_y))

    # Infer the model signature
    pred_y = model.predict(train_x)
    signature = infer_signature(train_x, pred_y)

    # Log model to Mlfow Model Registry
    mlflow.sklearn.log_model(
        artifact_path= MODEL_NAME,
        sk_model = model,
        signature=signature,
        registered_model_name=MODEL_NAME
    )
    
train_gboost()