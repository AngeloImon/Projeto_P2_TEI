import requests

FIREBASE_PROJECT_ID = 'projeto-p2-tei'
FIREBASE_API_KEY = "AIzaSyDhKeTBWb8vP0-glvanMx_-W2NNnBat0L0"

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