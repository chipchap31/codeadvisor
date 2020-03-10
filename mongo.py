# -----------------------------------------------------------

# -----------------------------------------------------------
import os
import pymongo
from datetime import datetime
import bcrypt
import json
from bson.objectid import ObjectId
from functools import *


class Mongo:
    def __init__(self, url):
        """
        New connection to mongo is created we check if the connection
        was a success or else print the custom error.
        """
        self.error = False
        self.registering = True
        self.register_error = {
            "user_name": False,
            "email": False,
            "password": False
        }
        self.login_error = {
            "user_name": False,
            "password": False
        }
        # define errors for view when registering

        try:

            client = pymongo.MongoClient(url)

            # select the development database
            # change this database when in production
            self.database = client["ms3_dev"]

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

        coll = self.database["users"]

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

        # new user model
        user_new = {
            "user_name": form_data["user_name"],
            "email": form_data["email"],
            "first_name": form_data["first_name"] or None,
            "last_name": form_data["last_name"] or None,
            "password": bcrypt.hashpw(str.encode(form_data["password"]), bcrypt.gensalt()),
            "registered": datetime.now(),
            "git_username": form_data['git_username']
        }

        coll.insert_one(user_new)

        return True  # true if there are no errors

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
        coll = self.database["users"]
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
        if self.error:
            return False
        # extract the data we want to save for the cookie

        cookie = {

            "_id": str(user_fetch["_id"]),
            "email": user_fetch["email"],
            "first_name": user_fetch["first_name"],
            "user_name": user_fetch["user_name"],
            "git_username": user_fetch['git_username']
        }

        return json.dumps(cookie) if not self.error else False

    def create_post(self, data):
        coll = self.database['posts']
        # determine if the post already exist in the collection
        find_post = coll.find_one({'_id': data['id']})

        if find_post:
            return False

        try:
            data = {
                '_id': data['id'],
                'name': data['name'],
                '_user': data['_user'],
                'stack_labels': data['stack_labels'],
                'stack_value': data['stack_value'],
                'description': data['description'],
                'updated_at': data['updated_at'],
                'homepage': data['homepage'],
                'html_url': data['html_url'],
                'language': data['language'],
                'feedbacks': [],
                'views': [],
                'posted_at': datetime.now()
            }
            coll.insert_one(data)
            return True
        except pymongo.errors.PyMongoError as e:
            print(e)
            return False

    def post_fetch(self, name='', user=False, sort='posted_at'):
        """

        :param name: string
        :param user: dict
        :param sort: str
        :param limit: int
        :rtype: list or dict
        """
        coll = self.database['posts']

        user = {'_user': user} if user else {}

        if not name:
            # if no user defined below, find all

            # check if sort is defined

            return list(coll.find(user).sort([(sort,  pymongo.DESCENDING)]))

        # the code block below finds a single post
        post = coll.find_one({'name': name})

        # avoid adding the username if the owner is viewing
        if post['_user'] != user['_user']:
            coll.update_one({'name': name}, {'$addToSet': {'views': user}})

        return post

    def data_delete(self, data):
        coll = self.database[data['collection']]

        try:
            # determine if the current has a valid username
            # delete if matches with id and username
            coll.delete_one({'_id': data['_id'], '_user': data['_user']})

            return True

        except pymongo.errors.PyMongoError as e:
            print(e)
            return False

    def create_feedback(self, data):
        """Inserts a feedback to a collection

            Args:
            data: dictionary to be inserted to feedback collection

            typical use:
                @ post_routes.py
                doc = {
                        'feedback': List,
                        'post_name': String,
                        'post_id': Number,
                        '_user': String,
                        'posted_at': Date(Str)
                    }
                database.create_feedback(doc)


            Returns:
                Boolean - true if success and then false if there
                are any errors.
        """
        feedbacks = self.database['feedbacks']
        posts = self.database['posts']
        try:
            # check if the user already added a comment on the selected feedback
            if feedbacks.find_one({'_user': data['_user'], 'post_name': data['post_name']}):
                return False

            # add the data to the feedback collectiosn
            feedback_doc = feedbacks.insert_one(data)
            feedback_id = str(feedback_doc.inserted_id)

            # update the post
            # add the id to the feedback field of the post
            # depending on the id
            posts.update_one({'_id': data['post_id']}, {'$addToSet': {
                'feedbacks': feedback_id
            }})

            return True
        except pymongo.errors.PyMongoError as e:
            print(e)
            return False

    def feedback_fetch(self, data):
        feedbacks = self.database['feedbacks']
        result = feedbacks.find(data)
        return result

    def feedback_impression(self, data):
        """
        typical use:
            {
                '_user': user['_id'],
                '_id': feedback_id,
                'impression': impression
            }
        """
        feedbacks = self.database['feedbacks']
        id = {"_id": ObjectId(data['_id'])}

        # check if the user id is already in like array
        like = bool(feedbacks.find_one({
            'like': {
                "$in": [data['_user']]
            },
            '_id': ObjectId(data['_id'])
        }))

        if like and data['impression'] == 'like':

            feedbacks.update_one(id, {
                "$pull": {
                    "like": data['_user']
                }
            })
            return

        dislike = bool(feedbacks.find_one({
            'dislike': {
                "$in": [data['_user']]
            },
            '_id': ObjectId(data['_id'])
        }))
        # check if the dislike is already pressed
        if dislike and data['impression'] == 'dislike':
            feedbacks.update_one(id, {
                "$pull": {
                    "dislike": data['_user']
                }
            })
            return

        # if the user id is not yet added to like or dislike
        feedbacks.update_one(id,
                             {'$addToSet' if data['impression'] == 'like' else '$pull': {
                                 "like": data['_user']
                             },
                                 '$addToSet' if data['impression'] == 'dislike' else '$pull': {
                                 'dislike': data['_user']
                             }})

        return True

    def fetch_user(self, user_name):
        user_collection = self.database['users']
        post_collection = self.database['posts']
        feeback_collection = self.database['feedbacks']

        user_fetch = user_collection.find_one({"user_name": user_name})
        if not user_fetch:
            return False
        curr_user = {
            "first_name": user_fetch['first_name'],
            "last_name": user_fetch['last_name'],
            "email": user_fetch['email'],
            "registered": user_fetch['registered'],
            "git_username": user_fetch['git_username'],
            "user_name": user_fetch['user_name']
        }

        # fetch the posts of the user
        post_amount = post_collection.find({'_user': user_name}).count()
        feedback_amount = feeback_collection.find(
            {'_username': user_name}).count()
        feedback_info = tuple(feeback_collection.aggregate([
            {
                "$match": {
                    "_username": user_name
                }
            },
            {

                "$project": {
                    "like_amount": {"$size": "$like"},
                    "dislike_amount": {"$size": "$dislike"}
                }
            }


        ]))
        # get the amount of likes and dislikes

        def getTotal(target):
            arr = map(lambda x: x[target], feedback_info)
            return reduce(lambda x, y: x + y, arr)

        return {
            **curr_user,
            "post_amount": post_amount,
            'feedback_amount': feedback_amount,
            'like_amount': getTotal('like_amount'),
            'dislike_amount': getTotal('dislike_amount')
        }

    def get_top_advisor(self):
        feedback_collection = self.database['feedbacks']
        """
        
        below we fetch the all of the feedbacks
        call the function $project to return 
        an object { 'like_amount': size of each of like array, 
        'user_name': users given username
        }
        """
        feedback_aggregate = tuple(feedback_collection.aggregate([
            {
                "$project": {
                    "like_amount": {
                        "$size": "$like"
                    },
                    "user_name": "$_username"
                }
            }
        ]))

        # get all of the user names
        unique_users = tuple(
            set(map(lambda x: x['user_name'], feedback_aggregate)))

        result = []

        for user in unique_users:
            # get the total likes for each user
            array = tuple(filter(
                lambda x: x['user_name'] == user, feedback_aggregate))

            like_info = reduce(lambda x, y: {
                'user_name': x['user_name'],
                'like_amount': x['like_amount'] + y['like_amount']
            }, array)

            result.append(like_info)
        print(result)

        print()

        if not any(x['like_amount'] > 0 for x in result):
            return []
        return sorted(result, key=lambda x: x['like_amount'], reverse=True)[:4]


#  we initialize a new connection to mongodb
# we export this so that it is reusable
database = Mongo(os.environ.get("MONGO_URI"))
