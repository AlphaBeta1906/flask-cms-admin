from flask import abort
from flask_login import current_user
from functools import wraps


def is_admin(func):
    """check if user email is admin"""

    @wraps(func)
    def check(*args, **kwargs):
        if (
            current_user.is_authenticated and not current_user.role == "admin"
        ) or not current_user.is_authenticated:
            return abort(404)
        return func(*args, **kwargs)

    return check


def get_start(page, limit=10):
    """
    get start of query by page number
    """
    start = 0
    if page > 1:
        start = page * limit - limit
    return start
