import os
import requests

URL = "http://127.0.0.1:8000/download/"

data = {
    # "url": "https://www.youtube.com/watch?v=W10RXr9c44Y"
    "url": "https://www.youtube.com/watch?v=ZhRQa8wTsW8"
}

response = requests.post(URL, json=data)
print(response)