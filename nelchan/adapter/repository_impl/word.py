from __future__ import annotations

from typing import Optional

from firebase_admin.firestore import firestore
from nelchan.domain.model import Word
from nelchan.domain.repository import WordRepository
from nelchan.infrasturcture.firestore import get_firestore_client


class WordRepositoryImpl(WordRepository):
    def __init__(self, project_id: str, cached_dict: dict[str, str]):
        self.collection: firestore.AsyncCollectionReference = get_firestore_client(
            project_id
        ).collection("dictionary")

        self.cached_dict = cached_dict

    async def get_by_keyword(self, keyword: str) -> Optional[Word]:
        if not keyword in self.cached_dict.keys():
            return None

        return Word(key=keyword, value=self.cached_dict[keyword])

    async def create_or_update(self, key: str, value: str) -> None:
        if not key in self.cached_dict.keys():
            await self.collection.document().set({"key": key, "value": value})
        else:
            words = self.collection.where("k")
            await words[0].reference.set({"key": key, "value": value})

    async def delete(self, key: str) -> None:
        self.collection.where("key", "==", key).delete()

    @classmethod
    async def create_with_cache(cls, project_id) -> WordRepositoryImpl:
        collection = firestore.AsyncCollectionReference = get_firestore_client(
            project_id
        ).collection("dictionary")
        cached_dict = {
            doc.get("key"): doc.get("value") for doc in await collection.stream()
        }
        return cls(project_id, cached_dict)


class WordRepositoryImplForDev(WordRepository):
    def __init__(self):
        self.keyword_dict: dict = dict()

    async def get_by_keyword(self, keyword: str) -> Optional[Word]:
        if not keyword in self.keyword_dict.keys():
            return None
        return Word(key=keyword, value=self.keyword_dict[keyword])

    async def create_or_update(self, key: str, value: str) -> None:
        self.keyword_dict[key] = value

    async def delete(self, key: str) -> None:
        del self.keyword_dict[key]
