import requests

flowers = [
    [6, 3, 5, 2],
    [5, 3, 4, 3],
    [4, 5, 2, 4]
]
response = requests.post("http://localhost:8000/", json=flowers)

flower_preditions = response.text

print(flower_preditions)