import os
import requests

URL = f"http://127.0.0.1:8000/send_post/?url=https://www.youtube.com/watch?v=UaSdM_hndRg&dest=ko" # en, ja, ko, zh
response = requests.post(URL)