import json
import os
import requests


def git_request(r):
    """
    creates a request to the github api
    :param r: str
        this is the route of the request
    :return: object | array
    """

    r = requests.get(
        f"https://api.github.com{r}",
        headers={
            "Authorization": os.environ.get("GIT_TOKEN")
        },
    )

    if r.status_code == 404:
        return False

    return json.loads(r.text)
