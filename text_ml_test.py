import requests

english_text = (
    "It was the best of times, it was the worst of times, it was the age "
    "of wisdom, it was the age of foolishness, it was the epoch of belief"
)
response = requests.post("http://kubernetes.patrick-cloud.com/summarize_translate/", json=english_text)
print(response)
french_text = response.text

print(french_text)