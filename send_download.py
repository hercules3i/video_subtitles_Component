import os
import requests

URL = "http://127.0.0.1:8000/download/"

data = {
    # "url": "https://www.youtube.com/watch?v=W10RXr9c44Y"
    "url": "https://www.youtube.com/watch?v=-67hh86N42Q"
}

response = requests.post(URL, json=data)
print(response)