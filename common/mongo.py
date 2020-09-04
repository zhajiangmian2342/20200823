
from pymongo import MongoClient


class Mongo():

    def __init__(self, host="localhost", port=27017):
        self.client = MongoClient(host=host, port=port)

    def insert(self, database, collection, document):
        """
        :param database:
        :param collection:
        :param document:
        :return:
        """
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        if isinstance(document, dict):
            result = _collection.insert_one(document)
            return result.inserted_id
        else:
            result = _collection.insert_many(document)
            return result.inserted_ids

    def delete(self, database, collection, filter):
        """
        :param database:
        :param collection:
        :param filter:
        :return:
        """
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        result = _collection.delete_many(filter)
        return result.deleted_count

    def update(self, database, collection, filter, document):
        """
        :param database:
        :param collection:
        :param filter:
        :param document:
        :return:
        """
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        result = _collection.update_many(filter, {"$set": document})
        return result.modified_count

    def search(self, database, collection, filter):
        """
        :param database:
        :param collection:
        :param filter:
        :return:
        """
        try:
            skip = int(filter.pop('page'))
        except TypeError:
            skip = 0
        except KeyError:
            skip = 0

        try:
            limit = int(filter.pop('limit'))
        except TypeError:
            limit = 20
        except KeyError:
            limit = 20

        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        results = list(_collection.find(filter, skip=skip, limit=limit))
        return results

    def aggregate(self, database, collection, pipeline):
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        return list(_collection.aggregate(pipeline))


if __name__ == '__main__':
    pass