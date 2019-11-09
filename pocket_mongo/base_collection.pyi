from pymongo.collection import Collection
from pymongo.results import DeleteResult
from typing import Any
from bson import ObjectId

class BaseCollection:
    collection: Collection

    @classmethod
    def by_id(cls, _id: Any) -> dict: ...

    @classmethod
    def delete_by_id(cls, _id: [str, ObjectId]) -> DeleteResult: ...