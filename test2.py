import os
import requests

URL = f"http://localhost:8000/generate/W10RXr9c44Y?dest=en" # en, ja, ko, zh
response = requests.post(URL)