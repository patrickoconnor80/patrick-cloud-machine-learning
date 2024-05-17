import requests

english_text = (
    "It was the best of times, it was the worst of times, it was the age "
    "of wisdom, it was the age of foolishness, it was the epoch of belief"
)
response = requests.post("https://kubernetes.patrick-cloud.com/ray-service-serve/", json=english_text)

french_text = response.text

print(french_text)