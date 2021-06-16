from functools import lru_cache
from urllib.parse import quote_plus

import firebase_admin
from firebase_admin import credentials, firestore


@lru_cache
def get_firestore_client(project_id: str) -> AsyncIOMotorDatabase:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(
        cred,
        {
            "projectId": project_id,
        },
    )
    return firestore.firestore.AsyncClient()
