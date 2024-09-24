import os
import requests

URL = f"http://localhost:8000/generate/W10RXr9c44Y?dest=ja" # en, ja, ko, zh
response = requests.post(URL)