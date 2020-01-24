"""
A custom mongoDB written in python via connected using pymongo

Author: Jomari Alang
"""
from pymongo import MongoClient
from datetime import datetime
import bcrypt


class Mongo:
    def __init__(self, url):
        try:
            client = MongoClient(url)
            self.db = client["ms3_dev"]

            print("Mongo is connected!")

            return None
        except pymongo.errors.ConnectionFailure as e:
            print("Could not connect to MongoDB %s" % e)
