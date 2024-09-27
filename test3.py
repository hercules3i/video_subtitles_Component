import os
import requests

URL = f"http://127.0.0.1:8002/send_post/?url=https://www.youtube.com/watch?v=W10RXr9c44Y&dest=en" # en, ja, ko, zh
response = requests.post(URL)