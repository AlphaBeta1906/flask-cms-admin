from flask import Blueprint, url_for
from flask_login import current_user

_filter = Blueprint("filter", __name__)


@_filter.app_template_filter("avatar")
def avatar_create(email, size=32):
    """function to generate gravatar avatar"""
    from hashlib import md5

    digest = md5(email.lower().encode("utf-8")).hexdigest()
    return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(digest, size)


@_filter.app_template_filter("url")
def url(url, **kwargs):
    return url_for(url, **kwargs)


@_filter.app_template_filter("static")
def static(filename):
    return url_for("static", filename=filename)
