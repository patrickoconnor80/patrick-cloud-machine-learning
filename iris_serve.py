from starlette.requests import Request
from typing import Dict

from ray import serve
import mlflow

TRACKING_URL = "https://kubernetes.patrick-cloud.com/mlflow/"
EXPERIMENT_NAME = "iris_gradient_boost_classifier_experiment"
MODEL_NAME = "iris_gradient_boost_classifier_model"

@serve.deployment
class Iris:
    def __init__(self):
        # Set up Mlflow and load model
        mlflow.set_tracking_uri(TRACKING_URL)
        self.model = mlflow.sklearn.load_model(model_uri=f"models:/{MODEL_NAME}/latest")

    def predict(self, lst: list) -> str:
        # Run inference
        prediction_lst = self.model.predict(lst)

        output = ""
        for index in range(len(lst)):
            prediction = prediction_lst[index]
            if prediction == 0:
                flower = 'Setosa'
            elif prediction == 1:
                flower =  'Vericolor'
            elif prediction == 2:
                flower = 'Virginica'
            else:
                flower = f'Unknown(prediction={prediction})'
            output += f"The ML Model predicts a flower with sepal length {lst[index][0]}, sepal width {lst[index][1]} and petal length {lst[index][2]} is a {flower} flower.\n"

        return output

    async def __call__(self, http_request: Request) -> str:
        image: str = await http_request.json()
        result = self.predict(image)

        return result

app = Iris.bind()