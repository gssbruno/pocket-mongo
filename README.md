# Pocket Mongo

An easy-to-use and quick setup interface for MongoDB.

Pocket Mongo was build to help developers manage collections, and their methods, in a single class.
Allows full access to `pymongo` API 
while offering customizable methods for implementing the business rules associated with the collection.  

## Getting Started

### Installing

```bash
pip install pocket-mongo
```

### Examples


Lets say you need a collection to store some cars informations:


```python
from pocket_mongo import BaseCollection

class Cars(BaseCollection):
    collection_name = 'cars'

Cars.collection.insert_many([
    {
        'car': 'Ford Torino',
        'horsepower': 140.,
        'origin': 'US',
    },
    {
        'car': 'Volvo 145e',
        'horsepower': 112.,
        'origin': 'Europe',
    },
    {
        'car': 'Chevrolet Impala',
        'horsepower': 150.,
        'origin': 'US',
    },
])
```

Now you can implement methods to query, insert and perform aggregations on that collection:

```python
class Cars(BaseCollection):
    collection_name = 'cars'

    @classmethod
    def get_us_only(cls) -> List[Dict]:
        return cls.collection.find({'origin': 'US'})
```

