from fastapi import Form, File, UploadFile, Request, FastAPI
import uvicorn
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import json
from schemas import LoginCredetials, TaskSchema, GetTaskSchema
from utils import update_recorded_status, find_unfinished_task, save_recording

# Use a service account.
cred = credentials.Certificate('firebase_jey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
textDb_colRef = db.collection('text-database')
userDb_colRef = db.collection('users')


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]
app = FastAPI(middleware=middleware)

@app.post("/api/login")
def login(credentials: LoginCredetials):
    user_doc = userDb_colRef.document(credentials.username).get()
    print(user_doc.to_dict())
    if user_doc.exists:
        if user_doc.to_dict()["password"] == credentials.password:
            return {"result": "success"}
        else:
            return {"result": "password incorrect"}
    else:
        return {"result": "no user with such username"}

# this is for testing purposes
def get_subject_dict(username:str):
    user_doc = userDb_colRef.document(username).get()
    user_dict = user_doc.to_dict()
    last_subject = user_dict["last-element"]["subject"]
    subject_dict = textDb_colRef.document(last_subject).get().to_dict()
    return  subject_dict

@app.post("/api/get-task")
def get_task(params: GetTaskSchema):
    user_doc = userDb_colRef.document(params.username).get()
    if not user_doc.exists:
        return {"result": "fail"}
    user_dict = user_doc.to_dict()
    last_element = user_dict["last-element"]
    try:
        next_element = find_unfinished_task(textDb_colRef=textDb_colRef,
                                            subject=last_element["subject"])
        if next_element==None:
            return {"error": "inside try, could not find unfinished task!"}
        else:
            return next_element

    except Exception as e:
        return {"error": "could not find unfinished task!","exception":str(e)}


@app.post("/api/upload-sound")
def upload_sound_record(username: str = Form(...),
                        subject: str = Form(...),
                        id: str = Form(...),
                        file: UploadFile = File(...)):
    print(username, subject, id)
    try:
        subject_docRef = textDb_colRef.document(subject)
        save_res = save_recording(docRef=subject_docRef,
                                id=id,
                                file=file)
        user_docRef = userDb_colRef.document(username)
        user_docRef.set({"last-element": {"subject": subject, "id": id}}, merge=True)
        return {"result": "success"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/")
def home():
    subject_dict = get_subject_dict("dummy")
    return subject_dict

@app.get("/")
def home():
    return {"hello": "world"}

if __name__ == "__main__":
    uvicorn.run(app,  port=8000)
