from typing import Optional

from firebase_admin.firestore import firestore
from nelchan.domain.model import Word
from nelchan.domain.repository import WordRepository
from nelchan.infrasturcture.firestore import get_firestore_client


class WordRepositoryImpl(WordRepository):
    def __init__(self, project_id):
        self.collection: firestore.AsyncCollectionReference = get_firestore_client(
            project_id
        ).collection("dictionary")

    async def get_by_keyword(self, keyword: str) -> Optional[Word]:
        word = await self.collection.where("key", "==", keyword).get()
        if not word:
            return None
        word = word[0]
        return Word(key=word.get("key"), value=word.get("value"))

    async def create_or_update(self, key: str, value: str) -> None:
        word = await self.collection.where("key", "==", key).get()
        if not word:
            await self.collection.document().set({"key": key, "value": value})
        else:
            await word[0].reference.set({"key": key, "value": value})

    async def delete(self, key: str) -> None:
        self.collection.where("key", "==", key).delete()


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
