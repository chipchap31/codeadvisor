import json


def require_login(cookies):
    try:
        return json.loads(cookies["user_data"])
    except:
        return False
