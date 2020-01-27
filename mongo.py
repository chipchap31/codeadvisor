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
import json


class Mongo:
    def __init__(self, url):
        """
        New connection to mongo is created we check if the connection
        was a success or else print the custom error.
        """
        self.error = False
        self.registering = True
        # define errors for users when registering

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
        # define errors for the user
        self.register_error = {
            "user_name": False,
            "email": False,
            "password": False
        }
        # reset current data
        self.error = False

        coll = self.db["users"]

        # check if user is registered already
        if coll.find_one({"user_name": form_data["user_name"]}):

            self.error = True
            self.register_error["user_name"] = "Username provided already exist"

        if coll.find_one({"email": form_data["email"]}):

            self.error = True
            self.register_error["email"] = "Email provided already exist"

        if len(form_data["password"]) < 11:

            self.error = True
            self.register_error["password"] = "Password must contain more than 10 characters"
            if form_data["password"] != form_data["password2"]:

                self.error = True
                self.register_error["password"] = "Passwords does not match"

        if self.error:
            # error is not triggered or error is false
            return False

        user_new = {
            "user_name": form_data["user_name"],
            "email": form_data["email"],
            "first_name": form_data["first_name"] or None,
            "last_name": form_data["last_name"] or None,
            "password": bcrypt.hashpw(str.encode(form_data["password"]), bcrypt.gensalt()),
            "registered": datetime.now()
        }

        coll.insert_one(user_new)
        return True

    def fetch_error(self):
        if self.registering:
            return self.register_error
        return self.login_error

    def login_user(self, form_data):
        self.registering = False
        self.login_error = {
            "user_name": False,
            "password": False
        }
        coll = self.db["users"]
        user_fetch = coll.find_one({"user_name": form_data["user_name"]})

        # reset error catcher

        self.error = False

        # if no user found
        if not user_fetch:
            self.error = True
            self.login_error["user_name"] = "Account does not exist"

        # if user found but the password does not match

        if user_fetch:

            if not bcrypt.checkpw(str.encode(form_data["password"]), user_fetch["password"]):
                self.error = True
                self.login_error["password"] = "Password does not match our record"

        # return the user found if didn't catch any error
        # extract the data we want to save for the cookie
        cookie = {

            "_id": str(user_fetch["_id"]),
            "email": user_fetch["email"],
            "first_name": user_fetch["first_name"],
            "user_name": user_fetch["user_name"]

        }

        return json.dumps(cookie) if not self.error else False
