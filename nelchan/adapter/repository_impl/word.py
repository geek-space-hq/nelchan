from __future__ import annotations

import os
from typing import Optional

from firebase_admin.firestore import firestore
from nelchan.domain.model import Word
from nelchan.domain.repository import WordRepository
from nelchan.infrasturcture.firestore import (
    get_firestore_client,
    get_firestore_client_sync,
)


class WordRepositoryImpl(WordRepository):
    def __init__(self, cached_dict: dict[str, str]):
        env = os.environ["ENV"]

        collection_name = "dictionary" if env == "prod" else "test_dictionary"
        self.collection: firestore.AsyncCollectionReference = (
            get_firestore_client().collection(collection_name)
        )

        self.cached_dict = cached_dict

    async def get_by_keyword(self, keyword: str) -> Optional[Word]:
        if not keyword in self.cached_dict.keys():
            return None

        return Word(key=keyword, value=self.cached_dict[keyword])

    async def create_or_update(self, key: str, value: str) -> None:
        if not key in self.cached_dict.keys():
            await self.collection.document().set({"key": key, "value": value})
            self.cached_dict[key] = value
        else:
            words = await self.collection.where("key", "==", key).get()
            await words[0].reference.set({"key": key, "value": value})
            self.cached_dict[key] = value

    async def delete(self, key: str) -> None:
        doc = await self.collection.where("key", "==", key).get()
        await doc[0].reference.delete()
        del self.cached_dict[key]
    @classmethod
    def create_with_cache(cls) -> WordRepositoryImpl:
        env = os.environ["ENV"]

        collection_name = "dictionary" if env == "prod" else "test_dictionary"
        collection = (
            firestore.CollectionReference
        ) = get_firestore_client_sync().collection(collection_name)
        cached_dict = {doc.get("key"): doc.get("value") for doc in collection.stream()}
        return cls(cached_dict)
