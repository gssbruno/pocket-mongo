import unittest
from bson import ObjectId
from pocket_mongo import *


class MyTestCase(unittest.TestCase):
    def test_pocket_mongo(self) -> None:
        class CarC(BaseCollection):
            colecao_nome = 'car'

        with self.assertRaises(PocketMongoConfigError):
            CarC.collection.insert_one({'Model': 'Audi'})

        address = 'mongodb://localhost:27027'
        database = 'unittest'

        Settings.config(address, database)

        self.assertEqual(address, Settings.address)
        self.assertEqual(database, Settings.database)

        car_id = CarC.collection.insert_one({'Model': 'BMW'})
        self.assertIsInstance(car_id.inserted_id, ObjectId)

        delete_count = CarC.delete_by_id(car_id.inserted_id).deleted_count
        self.assertEqual(delete_count, 1)


if __name__ == '__main__':
    unittest.main()
