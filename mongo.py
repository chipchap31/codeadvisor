# -----------------------------------------------------------
# demonstrates how to write ms excel files using python-openpyxl
#
# (C) 2015 Frank Hofmann, Berlin, Germany
# Released under GNU Public License (GPL)
# email frank.hofmann@efho.de
# -----------------------------------------------------------
from pymongo import MongoClient
from datetime import datetime
import bcrypt


class Mongo:
    def __init__(self, url):
        """
        New connection to mongo is created we check if the connection 
        was a success or else print the custom error.
        """

        try:
            client = MongoClient(url)

            # select the development database
            # change this database when in production
            self.db = client["ms3_dev"]

            print("Mongo is connected!")

            return None
        except pymongo.errors.ConnectionFailure as e:
            # print an error if the connection is a failure
            print("Could not connect to MongoDB %s" % e)

    def register_user(self, form_data):
        """
        This function creates a new user. 
        we check if the user is currently in the database

        """

        print(form_data)
