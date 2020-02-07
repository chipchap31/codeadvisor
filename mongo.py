# -----------------------------------------------------------

# -----------------------------------------------------------
import os
import pymongo
from datetime import datetime
import bcrypt
import json
from bson.objectid import ObjectId


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
            "role": None,
            "password": bcrypt.hashpw(str.encode(form_data["password"]), bcrypt.gensalt()),
            "registered": datetime.now(),
            "git_username": None
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
        # extract the data we want to save for the cookie
        cookie = {

            "_id": str(user_fetch["_id"]),
            "email": user_fetch["email"],
            "first_name": user_fetch["first_name"],
            "user_name": user_fetch["user_name"],
            "role": user_fetch["role"],
            "git_username": user_fetch['git_username']
        }

        return json.dumps(cookie) if not self.error else False

    def set_role(self, user_name: str, role: str):
        """
        Description
        ------------
        At this stage, user is already registered and logged in
        Allows user to set the role

        Parameters
        -----------

        user_name : str
            current user's username
        role : str

        """
        coll = self.database["users"]
        try:
            coll.update_one({'user_name': user_name}, {'$set': {"role": role}})
            return True
        except pymongo.errors.PyMongoError as e:
            print(e)
            return False

    def create_project(self, project_data, user_name):

        """
            Description
            --------------
            Creates new project if the role of the user is student

            Parameters
            --------------
            project_data : dict
                - contains the form data send from route '/project/new'
            model : {
                project_tile: str,
                site_url: str,
                front_end: list,
                description: str,
                back_end : str
            }
            user_name : str
                - current user's username

            Returns
            --------------
            bool
                - Returns True if data was saved successfully
                else creates an error

        """

        coll = self.database["projects"]

        # document to save in project collection

        doc = {
            "project_title": project_data['project_title'],
            "github_repo": project_data['github_repo'],
            "site_url": project_data['site_url'] or None,
            "front_end": project_data.getlist('front_end'),
            "back_end": project_data["back_end"] or None,
            "description": project_data["description"],
            "_user": str(user_name),
            "views": [],
            "created": datetime.now(),
            "feedbacks": []
        }
        try:
            coll.insert_one(doc)
            return True
        except pymongo.errors.PyMongoError:
            raise Exception("Failed to create new project")
            return False

    def fetch_projects(self, data):
        coll = self.database["projects"]

        query = {"_user": data['user']} if data['user'] else {}

        if data['sort'] == 'newest':
            return list(coll.find(query)
                        .limit(data['limit'] or 5)
                        .sort([('created', pymongo.DESCENDING)]))
        elif data['sort'] == "feedbacks":
            return list(coll.find(query)
                        .limit(data['limit'] or 5)
                        .sort([('feedbacks', pymongo.DESCENDING)]))

        elif data['sort'] == 'views':
            return list(coll.find(query)
                        .limit(data['limit'] or 5)
                        .sort([('views', pymongo.DESCENDING)]))

        else:
            return list(coll.find(query)
                        .limit(data['limit'] or 5)
                        .sort([('created', pymongo.ASCENDING)]))

    def project_single(self, project_id, user_id):
        """
            Uses project collection.

            Adds the user id to the 'view' field of a single project and

            Returns the single project depending on the '_id' field.

            Parameters
            ---------------
            project_id : string
                single project's id
            user_id : string
                current user's unique id

            Returns
            ---------------
            type: json

            model: {
            "_id": str,
            "_user": str,
            "back_end": str,
            "created": date,
            "description": str,
            "feedbacks": list,
            "front_end": list,
            "github_repo": str,
            "project_title": str,
            "site_url": str,
            "views": list
            }
        """
        coll = self.database['projects']
        try:
            coll.update_one({'_id': ObjectId(project_id)}, {'$addToSet': {"views": {"_user": ObjectId(user_id)}}})
            req = json.dumps(coll.find_one({'_id': ObjectId(project_id)}), indent=4, sort_keys=True, default=str)
            return json.loads(req)
        except pymongo.errors.PyMongoError as e:
            raise Exception(e)

    def project_delete(self, id: str):
        coll = self.database['projects']

        coll.delete_one({'_id': ObjectId(id)})
        return True

    def set_git_username(self, target, value):
        coll = self.database['users']
        try:
            coll.update_one({'user_name': target}, {'$set': {'git_username': value}})
            return True
        except pymongo.errors.PyMongoError as e:
            print(e)
            return False


#  we initialize a new connection to mongodb
# we export this so that it is reusable
database = Mongo(os.environ.get("MONGO_URI"))
