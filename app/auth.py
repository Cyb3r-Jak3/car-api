"""
Authentication for the app. Both secret header and basic auth.
Most of the HTTP basic authentication has been modified from Flask-BasicAuth
"""

import os
from functools import wraps

from flask import request, Response

BASIC_USERNAME = os.getenv("BASIC_AUTH_USER", None)
BASIC_PASSWORD = os.getenv("BASIC_AUTH_PASS", None)

SECRET_HEADER = os.getenv("SECRET_HEADER", None)


def handle_auth() -> bool:
    """
    Handle incoming request auth

    :return: If the request passes auth
    :rtype: bool
    """
    if request.headers.get("X-SECRET-HEADER"):
        return request.headers["X-SECRET-HEADER"] == SECRET_HEADER
    auth = request.authorization
    return (
        auth
        and auth.type == "basic"
        and auth.username == BASIC_USERNAME
        and auth.password == BASIC_PASSWORD
    )


def challenge():
    """
    Challenge the client for username and password.

    This method is called when the client did not provide username and
    password in the request, or the username and password combination was
    wrong.

    :returns: a :class:`~flask.Response` with 401 response code, including
        the required authentication scheme and authentication realm.
    """
    return Response(
        status=401,
        headers={"WWW-Authenticate": f'Basic realm="{os.getenv("BASIC_REALM")}"'},
    )


def auth_needed(view_func):
    """
    A decorator that can be used to protect specific views with authentication.
    """

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if handle_auth():
            return view_func(*args, **kwargs)
        return challenge()

    return wrapper
