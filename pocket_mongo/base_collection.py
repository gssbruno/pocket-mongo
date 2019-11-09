from typing import Any
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from bson import ObjectId
from .exceptions import PocketMongoConfigError
from .settings import Settings

__all__ = [
    'BaseCollection'
]


class Meta(type):
    colecao_nome = None
    db: Database

    def __init__(cls, *args, **kwargs):
        cls.validar_collection(args)
        cls._colecao: Collection = None

        super().__init__(*args, **kwargs)

    @property
    def collection(cls) -> Collection:
        if not cls._colecao:
            cls.criar_colecao()

        return cls._colecao

    def validar_collection(cls, args: tuple) -> None:
        if args[0] != 'colecaoBase' and not args[2].get('colecao_nome'):
            raise ValueError(
                'Classe %s precisa definir uma <colecao_nome>' % args[2]
            )

    def criar_colecao(cls) -> Collection:
        """
        Retorna a instância da coleção referente à classe definida.

        :return:
        """
        cls.validate_settings()
        cls.db = MongoClient(Settings.address)[Settings.database]
        cls._colecao = cls.db[cls.colecao_nome]
        cls.create_indexes()

    def create_indexes(cls) -> None:
        if hasattr(cls, 'indices'):
            cls.collection.create_indexes(cls.indices)

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
    colecao_nome = 'colecaoBase'

    @classmethod
    def by_id(cls, _id: Any) -> dict:
        """
        Método helper para retornar um documento a partir de sua _id.

        :param _id: _id do documento no MongoDB
        :return:
        """
        if isinstance(_id, str):
            _id = ObjectId(_id)

        return cls.collection.find_one({'_id': _id})

    @classmethod
    def delete_by_id(cls, _id: Any) -> int:
        if isinstance(_id, str):
            _id = ObjectId(_id)

        return cls.collection.delete_one({'_id': _id})
