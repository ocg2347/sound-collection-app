import json
import uuid
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def main():
    # open the dataset json:
    dataset = json.load(open("dataset.json", "r"))["data"]

    database = {}
    # Use a service account.
    cred = credentials.Certificate('firebase_jey.json')
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    col_ref = db.collection('text-database')

    n_subject = 5000
    n_task = 3000
    n_qa = 2000
    i_s = 0
    for subject in dataset:
        i_s+=1
        if i_s>=n_subject:
            break

        title = subject["title"]
        task_list = []

        
        # iterate over paragraphs:
        for task in subject["paragraphs"]:  # paragraph:dict
            if len(task_list)>=n_task:
                break
            context = task["context"]
            context_id = str(uuid.uuid4())
            task_dict = {}
            task_dict["context"] = {
                "id": context_id,
                "text": context,
                "recorded": False

            }
            task_dict["qas"] = []
            for qa in task["qas"]:
                if len(task_dict["qas"])>=n_qa:
                    break
                task_dict["qas"].append(
                    {
                        "question": {
                            "id": qa["id"]+"_q",
                            "text": qa["question"],
                            "recorded": False
                        },
                        "answer": {
                            "id": qa["id"]+"_a",
                            "text": qa["answers"][0]["text"],
                            "recorded": False
                        }
                    }
                )
            task_list.append(task_dict)
        database[title] = task_list
        col_ref.document(title).set({
            "assigned":False,
            "task_list": task_list})
    open("db.json", "w").write(json.dumps(database, indent=4))


if __name__ == '__main__':
    main()
