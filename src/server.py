from fastapi import Form, File, UploadFile, Request, FastAPI
import uvicorn
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import json
from schemas import LoginCredetials, TaskSchema, GetTaskSchema
from utils import update_recorded_status, find_unfinished_task, save_recording, get_new_subject

# Use a service account.
cred = credentials.Certificate('firebase_jey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
textDb_colRef = db.collection('text-database')
userDb_colRef = db.collection('users')
N_SUBJECT_PER_USER = 4

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
    # return {"message": "hello world"}
    user_doc = userDb_colRef.document(params.username).get()
    if not user_doc.exists:
        return {"message": ":S user does not exist"}
    user_dict = user_doc.to_dict()
    last_element = user_dict["last-element"]
    try:
        next_element = find_unfinished_task(textDb_colRef=textDb_colRef,
                                            subject=last_element["subject"])
        if next_element==None: # if no task left in the current subject, try to switch to the next subject
            # update user's done-subjects list
            user_docRef = userDb_colRef.document(params.username)
            user_docRef.set({"done-subjects": firestore.ArrayUnion([last_element["subject"]])}, merge=True)
            # now check if user already finished her max n subjects:
            if len(user_dict["done-subjects"])>=N_SUBJECT_PER_USER:
                return {"message":"you have done all your tasks mate. thank you!"}
            # if not, switch to the next subject
            new_subject = get_new_subject(textDb_colRef)
            if new_subject!=None:
                next_element = find_unfinished_task(textDb_colRef=textDb_colRef,
                                                    subject=new_subject)
                user_docRef = userDb_colRef.document(params.username)
                user_docRef.set({"last-element": {"subject": new_subject, "id": next_element.id}}, merge=True)
                return next_element
            else:
                return {"message":"you have done all your tasks mate. thank you!"}
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
        print(e)
        return {"result": "fail"}


@app.get("/api/test")
def home():
    return {"hello": "world"}

# add user to the database method. only input is the username
@app.post("/api/add-user")
def add_user(username: str = Form(...)):
    # check if user already exists
    user_doc = userDb_colRef.document(username).get()
    if user_doc.exists:
        return {"result": "user already exists"}
    # create new user
    user_docRef = userDb_colRef.document(username)
    # get a new subject
    new_subject = get_new_subject(textDb_colRef)
    if new_subject!=None:
        # assign the new subject to the user
        textDb_colRef.document(new_subject).set({"assigned":True}, merge=True)
        user_docRef.set({"password":"abcde", "last-element": {"subject": new_subject, "id": ""}}, merge=True)
        return {"result": "success"}
    else:
        return {"result": "no more subjects left"}

@app.get("/")
def home():
    return {"hello": "world"}

if __name__ == "__main__":
    uvicorn.run(app,  host="0.0.0.0", port=8000)