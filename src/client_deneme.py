import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

resp = requests.request(
    "POST",
#    url="http://127.0.0.1:8000/get-task",
    url="http://127.0.0.1:8000/login",
    data=json.dumps({
        "username": "dummy",
        "password": "genel",
    }),
)
print(resp.text)
