from ray import serve

import pickle
import json
import numpy as np
import os
import tempfile
from starlette.requests import Request
from typing import Dict

from sklearn.datasets import load_iris
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import mean_squared_error

import mlflow
from ray.air.integrations.mlflow import MLflowLoggerCallback, setup_mlflow

TRACKING_URL = "https://kubernetes.patrick-cloud.com/mlflow/"
EXPERIMENT_NAME = "iris_gradient_boost_classifier"

def train_gboost():


    mlflow.set_tracking_uri(TRACKING_URL)
    mlflow.set_experiment(EXPERIMENT_NAME)
    mlflow.autolog()
    setup_mlflow(
        tracking_uri = TRACKING_URL,
        expiriment_name = EXPERIMENT_NAME
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
    mlflow.log_metric(key="MSE:", val=mean_squared_error(model.predict(val_x), val_y))

# # Save the model and label to file
# MODEL_PATH = os.path.join(
#     tempfile.gettempdir(), "iris_model_gradient_boosting_classifier.pkl"
# )
# LABEL_PATH = os.path.join(tempfile.gettempdir(), "iris_labels.json")

# with open(MODEL_PATH, "wb") as f:
#     pickle.dump(model, f)
# with open(LABEL_PATH, "w") as f:
#     json.dump(target_names.tolist(), f)