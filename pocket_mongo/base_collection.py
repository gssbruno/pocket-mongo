from typing import *
from pymongo import MongoClient, IndexModel
from pymongo.collection import Collection
from pymongo.database import Database
from bson import ObjectId
from .exceptions import PocketMongoConfigError, PocketMongoCollectionNotDefined
from .settings import Settings

__all__ = [
    'BaseCollection'
]


class Meta(type):
    collection_name: str = None
    indexes: List[IndexModel] = None
    db: Database

    def __init__(cls, *args, **kwargs):
        cls.validate_collection(args)
        cls._collection: Collection = None

        super().__init__(*args, **kwargs)

    @property
    def collection(cls) -> Collection:
        if not cls._collection:
            cls.create_collection()

        return cls._collection

    def validate_collection(cls, args: tuple) -> None:
        if args[0] != 'colecaoBase' and not args[2].get('collection_name'):
            raise PocketMongoCollectionNotDefined(args[2])

    def create_collection(cls) -> Collection:
        cls.validate_settings()
        cls.db = MongoClient(Settings.address)[Settings.database]
        cls._collection = cls.db[cls.collection_name]
        cls.create_indexes()

    def create_indexes(cls) -> None:
        if cls.indexes is not None:
            cls.collection.create_indexes(cls.indexes)

    def validate_settings(cls):
        if not Settings.address:
            raise PocketMongoConfigError(
                'address not defined'
            )

        if not Settings.database:
            raise PocketMongoConfigError(
                'database not defined'
            )


class BaseCollection(metaclass=Meta):
    collection_name = 'colecaoBase'

    @classmethod
    def by_id(cls, _id: Any) -> dict:
        """
        Helper method that returns a document by its _id.

        :param _id: Document ObjectId, or its string value
        :return:
        """
        if isinstance(_id, str):
            _id = ObjectId(_id)

        return cls.collection.find_one({'_id': _id})

    @classmethod
    def delete_by_id(cls, _id: Any) -> int:
        """
        Helper method that deletes a document by its _id.

        :param _id: Document ObjectId, or its string value.
        :return:
        """
        if isinstance(_id, str):
            _id = ObjectId(_id)

        return cls.collection.delete_one({'_id': _id}).deleted_count

    @classmethod
    def objects(cls, _filter: Dict = None):
        if not _filter:
            _filter = {}

        docs = cls.collection.find(_filter)

        return [cls(**doc) for doc in docs]

    def __init__(self, *args, **kwargs) -> None:
        self.id = kwargs.get('_id', None)

    def delete(self) -> int:
        return self.delete_by_id(self.id)

    @property
    def id_filtro(self) -> dict:
        return {'_id': self.id}

    def save(self) -> ObjectId:
        doc = self.__dict__.copy()

        doc.pop('id')
        if not hasattr(self, 'id') or not self.id:
            self.id = self.__class__.collection.insert_one(doc).inserted_id
            return self.id

        self.__class__.collection.update_one(self.id_filtro, {'$set': doc})
        return self.id
