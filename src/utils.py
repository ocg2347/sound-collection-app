from firebase_admin import firestore
from fastapi import UploadFile
from schemas import TaskSchema

def update_recorded_status(subject_dict: dict, id: str):
    for task in subject_dict["task_list"]:
        if task["context"]["id"] == id:
            task["context"]["recorded"] = True
            return subject_dict
        for qa in task["qas"]:
            if qa["question"]["id"] == id:
                qa["question"]["recorded"] = True
            if qa["answer"]["id"] == id:
                qa["answer"]["recorded"] = True
            if task["context"]["id"] == id:
                task["context"]["recorded"] = True
    return subject_dict


def find_unfinished_task(textDb_colRef: firestore.CollectionReference,
                        subject: str):
    subject_dict = textDb_colRef.document(subject).get().to_dict()
    isLastFound = False
    nParagraphs = len(subject_dict["task_list"])
    for i, paragraph in enumerate(subject_dict["task_list"]):
        if paragraph["context"]["recorded"]==False:
            return TaskSchema(
                id=paragraph["context"]["id"],
                text=paragraph["context"]["text"],
                subject=subject,
                type="context",
                paragraph=i,
                totalParagraphs=nParagraphs,
            )
        nQas = len(paragraph["qas"])
        for j, qa in enumerate(paragraph["qas"]):
            if qa["question"]["recorded"]==False:
                return TaskSchema(
                    id=qa["question"]["id"],
                    text=qa["question"]["text"],
                    subject=subject,
                    type="question",
                    paragraph=i,
                    totalParagraphs=nParagraphs,
                    question=j,
                    totalQuestions=nQas,
                )
            if qa["answer"]["recorded"]==False:
                return TaskSchema(
                    id=qa["answer"]["id"],
                    text=qa["answer"]["text"],
                    subject=subject,
                    type="answer",
                    paragraph=i,
                    totalParagraphs=nParagraphs,
                    question=j,
                    totalQuestions=nQas,
                )
    return None


def save_recording(docRef: firestore.DocumentReference,
                   id: str,
                   file: UploadFile):
    # save the file on local with id as name
    filename = f"{id}.wav"
    with open(filename, "wb") as buffer:
        buffer.write(file.file.read())
    # then update document
    docRef.set(
        update_recorded_status(
            subject_dict=docRef.get().to_dict(),
            id=id
            ))