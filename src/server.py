from fastapi import Form, File, UploadFile, Request, FastAPI
import uvicorn
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pydantic import BaseModel, Field
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware


class LoginCredetials(BaseModel):
    username: str
    password: str


class GetTaskSchema(BaseModel):
    username: str


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


@app.post("/login")
def login(credentials: LoginCredetials):
    user_doc = userDb_colRef.document(credentials.username).get()
    if user_doc.exists:
        if user_doc.to_dict()["password"] == credentials.password:
            return {"result": "success"}
        else:
            return {"result": "password incorrect"}
    else:
        return {"result": "no user with such username"}


def find_unfinished_task(subject_dict: dict, last_id: str):
    isLastFound = False
    for i, paragraph in enumerate(subject_dict["task_list"]):
        if isLastFound:
            return {
                "id": paragraph["context"]["id"],
                "task_idx": i
            }

        elif (paragraph["context"]["id"] == last_id):
            isLastFound = True
        else:
            for qa in paragraph["qas"]:
                q_id, a_id = qa["question"]["id"], qa["answer"]["id"]
                if isLastFound:
                    return {
                        "id": q_id,
                        "task_idx": i
                    }
                elif q_id == last_id:
                    isLastFound = True
                if isLastFound:
                    return {
                        "id": a_id,
                        "task_idx": i
                    }
                elif a_id == last_id:
                    isLastFound = True
    return None


# def save_recording(docref, id, file):
#     for x in docref.child("task_list")


@app.post("/get-task")
def get_task(params: GetTaskSchema):
    user_doc = userDb_colRef.document(params.username).get()
    if not user_doc.exists:
        return {"result": "fail"}
    user_dict = user_doc.to_dict()
    # nSubjectsTotal = len(user_dict["task_subjects"])
    # nFinished = len(user_dict["finished_subjects"])
    last_element = user_dict["last-element"]
    subject_dict = textDb_colRef.document(
        last_element["subject"]).get().to_dict()
    try:
        next_element = find_unfinished_task(
            subject_dict=subject_dict, last_id=last_element["id"])
        next_element["subject"] = last_element["subject"]
        return next_element
    except:
        return {"error": "could not find unfinished task!"}


@app.post("/upload-sound")
def upload_sound_record(subject: str = Form(...),
                        id: str = Form(...),
                        file: UploadFile = File(...)):
    subject_docRef = textDb_colRef.document(subject)
    save_res = save_recording(docRef=subject_docRef,
                              id=id,
                              file=file)


@app.get("/")
def home():
    return {"hello": "world"}


if __name__ == "__main__":
    uvicorn.run(app,  port=8000)
