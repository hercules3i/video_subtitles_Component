import os
import requests

URL = "http://localhost:8000/generate/ZhRQa8wTsW8?dest=ja"



response = requests.post(URL)
print(response)