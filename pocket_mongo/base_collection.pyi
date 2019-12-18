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
    id: ObjectId

    @classmethod
    def by_id(cls, _id: Any) -> dict: ...

    @classmethod
    def delete_by_id(cls, _id: [str, ObjectId]) -> DeleteResult: ...

    @classmethod
    def objects(cls, _filter: Dict): ...

    def __init__(self, *args, **kwargs): ...

    def save(self) -> ObjectId: ...

    def delete(self) -> int: ...

    def id_filtro(self) -> Dict: ...
