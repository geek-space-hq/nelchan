import os
from functools import lru_cache

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(
    cred,
    {
        "projectId": "nelchan",
    },
)


@lru_cache
def get_firestore_client() -> firestore.firestore.AsyncClient:
    return firestore.firestore.AsyncClient()


@lru_cache
def get_firestore_client_sync() -> firestore.firestore.Client:
    return firestore.firestore.Client()
