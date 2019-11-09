from pymongo import IndexModel
from pymongo.collection import Collection
from pymongo.results import DeleteResult
from pymongo.database import Database
from typing import *
from bson import ObjectId

class BaseCollection:
    collection: Collection
    collection_name: str
    indexes: List[IndexModel]
    db: Database

    @classmethod
    def by_id(cls, _id: Any) -> dict: ...

    @classmethod
    def delete_by_id(cls, _id: [str, ObjectId]) -> DeleteResult: ...