import os
import unittest
from pymongo import IndexModel
from bson import ObjectId
from pocket_mongo import *


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        Settings.config(None, None)

        class CarC(BaseCollection):
            collection_name = 'car'

        with self.assertRaises(PocketMongoConfigError):
            CarC.collection.insert_one({'Model': 'Gol'})

        address = os.getenv('MONGO_ADDRESS')
        database = os.getenv('DATABASE')

        Settings.config(address, database)

        self.assertEqual(address, Settings.address)
        self.assertEqual(database, Settings.database)

    def test_pocket_mongo(self) -> None:
        class CarC(BaseCollection):
            collection_name = 'car'

        car_id = CarC.collection.insert_one({'Model': 'BMW'})
        self.assertIsInstance(car_id.inserted_id, ObjectId)

        delete_count = CarC.delete_by_id(car_id.inserted_id)
        self.assertEqual(delete_count, 1)

    def test_indexes_creation(self) -> None:
        class LogC(BaseCollection):
            collection_name = 'log'
            indexes = [
                IndexModel([('creation_date', 1)])
            ]

        indexes = list(LogC.collection.list_indexes())
        self.assertEqual(2, indexes.__len__())

    def test_collection_not_defined(self) -> None:
        with self.assertRaises(PocketMongoCollectionNotDefined):
            class NoCollection(BaseCollection):
                pass

    def test_inheritance(self) -> None:
        class MobilePhoneC(BaseCollection):
            collection_name = 'mobilePhone'

            def __init__(self, model, *args, **kwargs):
                self.model = model
                super().__init__(*args, **kwargs)

            def __repr__(self) -> str:
                return f'Mobile Phone: {self.model}'

        mb = MobilePhoneC('IPhone11')
        mb.save()

        docs = MobilePhoneC.objects({})
        self.assertTrue(all([isinstance(d, MobilePhoneC) for d in docs]))

        self.assertEqual(1, mb.delete())


if __name__ == '__main__':
    unittest.main()
