import json


def require_login(cookies: object) -> object:
    """

    :rtype:
    """
    try:
        return json.loads(cookies["user_data"])
    except Exception as ex:
        print(ex)
        return False


def require_student(cookies, redirect):

    try:
        cookies = json.loads(cookies['user_data'])
        if cookies['role'] == 'student':
            return cookies
        else:
            return redirect('/login')

    except Exception as ex:
        print("Error: require_student(): %s" % ex)
        return False
