import requests
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db


import requests
usename = "dummy"
# adds new user:
resp = requests.request(
    "POST",
    url="http://ec2-54-82-21-40.compute-1.amazonaws.com:8000/api/add-user",
    data={
        "username": usename
    },
)
print(resp.json())
# resp = requests.request(
#     "POST",
#    url="http://127.0.0.1:8000/get-task",
#     # url="http://127.0.0.1:8000/login",
#     data=json.dumps({
#         "username": "dummy",
#         "password": "abcde",
#     }),
# )
# resp = resp.json()
# print(resp)
# id = resp["id"]
# subject = resp["subject"]
# print(id, subject)
# resp = requests.request(
#     "POST",
#    url="http://127.0.0.1:8000/upload-sound",
#    data={
#         "username": "dummy",
#         "subject": subject,
#         "id": id,
#         # "file": open("Recording.m4a", "rb"),
#    },
#    files={"file":open("Recording.m4a", "rb")}
# )
