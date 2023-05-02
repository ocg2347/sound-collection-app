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

    for subject in dataset:
        title = subject["title"]
        task_list = []

        # iterate over paragraphs:
        for task in subject["paragraphs"]:  # paragraph:dict
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
                task_dict["qas"].append(
                    {
                        "question": {
                            "id": qa["id"],
                            "text": qa["question"],
                            "recorded": False
                        },
                        "answer": {
                            "id": str(uuid.uuid4()),
                            "text": qa["answers"][0]["text"],
                            "recorded": False
                        }
                    }
                )
            task_list.append(task_dict)
        database[title] = task_list
        col_ref.document(title).set({"task_list": task_list})
    open("db.json", "w").write(json.dumps(database, indent=4))


if __name__ == '__main__':
    main()
