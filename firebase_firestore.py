import requests
import os
from dotenv import load_dotenv

load_dotenv()

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")

def firestore_set_user_data(uid, data, id_token):
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/usuarios/{uid}"
    headers = {"Authorization": f"Bearer {id_token}"}
    firestore_data = {
        "fields": {k: {"stringValue": str(v)} for k, v in data.items()}
    }
    response = requests.patch(url, json=firestore_data, headers=headers)
    return response.json()

def firestore_get_user_data(uid, id_token):
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/usuarios/{uid}"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = requests.get(url, headers=headers)
    return response.json()