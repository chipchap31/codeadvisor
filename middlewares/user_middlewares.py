import json


def require_login(cookies):
    """Gets the cookie from the browser and reads it as python"""
    try:
        return json.loads(cookies["user_data"])
    except Exception as ex:

        return False
