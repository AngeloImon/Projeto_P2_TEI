import requests
import os
from dotenv import load_dotenv

load_dotenv()

FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")


def firestore_get_user_plans(uid, id_token):
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/usuarios/{uid}/planos"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    data = response.json()
    planos = []
    for doc in data.get("documents", []):
        fields = doc.get("fields", {})
        planos.append(
            {
                "id": doc.get("name", "").split("/")[-1],
                "titulo": fields.get("titulo", {}).get("stringValue", ""),
                "descricao": fields.get("descricao", {}).get("stringValue", ""),
                "programacao": fields.get("programacao", {}).get("stringValue", ""),
                "horario": fields.get("horario", {}).get("stringValue", ""),
                "duracao": fields.get("duracao", {}).get("stringValue", ""),
                "cor": fields.get("cor", {}).get("stringValue", ""),
                "data_adicionado": fields.get("data_adicionado", {}).get(
                    "stringValue", ""
                ),
            }
        )
    return planos


def firestore_create_user_plan(uid, id_token, plano):
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/usuarios/{uid}/planos"
    headers = {
        "Authorization": f"Bearer {id_token}",
        "Content-Type": "application/json",
    }
    # Monta o corpo do documento Firestore
    fields = {
        "titulo": {"stringValue": plano.get("titulo", "")},
        "descricao": {"stringValue": plano.get("descricao", "")},
        "programacao": {"stringValue": plano.get("programacao", "")},
        "alerta": {"stringValue": plano.get("alerta", "")},
        "cor": {"stringValue": plano.get("cor", "")},
    }
    data = {"fields": fields}
    response = requests.post(url, headers=headers, json=data)
    return response.status_code == 200 or response.status_code == 202


def firestore_add_user_plan(uid, id_token, data):
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/usuarios/{uid}/planos"
    headers = {"Authorization": f"Bearer {id_token}"}
    firestore_data = {"fields": {k: {"stringValue": str(v)} for k, v in data.items()}}
    response = requests.post(url, json=firestore_data, headers=headers)
    return response.status_code == 200


def firestore_update_user_plan(uid, id_token, plan_id, data):
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/usuarios/{uid}/planos/{plan_id}"
    headers = {"Authorization": f"Bearer {id_token}"}
    firestore_data = {"fields": {k: {"stringValue": str(v)} for k, v in data.items()}}
    response = requests.patch(url, json=firestore_data, headers=headers)
    return response.status_code == 200


def firestore_delete_user_plan(uid, id_token, plan_id):
    url = f"https://firestore.googleapis.com/v1/projects/{FIREBASE_PROJECT_ID}/databases/(default)/documents/usuarios/{uid}/planos/{plan_id}"
    headers = {"Authorization": f"Bearer {id_token}"}
    response = requests.delete(url, headers=headers)
    return response.status_code == 200
