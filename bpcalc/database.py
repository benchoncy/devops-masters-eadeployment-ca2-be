import pymongo
import os

DATABASE_URI = os.environ.get('DATABASE_URI', None)
DATABASE_NAME = os.environ.get('DATABASE_NAME', None)
DATABASE_COLLECION = os.environ.get('DATABASE_COLLECTION', None)


if DATABASE_URI is not None:
    try:
        mongo_client = pymongo.MongoClient(DATABASE_URI)
        mongo_db = mongo_client[DATABASE_NAME]
        mongo_collection = mongo_db[DATABASE_COLLECION]
    except pymongo.errors.ConfigurationError:
        print("Could not connect to database.")
        exit(1)


def insert_document(document):
    try:
        mongo_collection.insert_one(document)
    except pymongo.errors.OperationFailure:
        print("Could not insert document.")
