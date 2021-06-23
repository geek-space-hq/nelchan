from functools import lru_cache

import firebase_admin
from firebase_admin import credentials, firestore

# from urllib.parse import quote_plus


@lru_cache
def get_firestore_client(project_id: str) -> firestore.firestore.AsyncClient:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(
        cred,
        {
            "projectId": project_id,
        },
    )
    return firestore.firestore.AsyncClient()


@lru_cache
def get_firestore_client_sync() -> firestore.firestore.Client:
    return firestore.firestore.Client()
