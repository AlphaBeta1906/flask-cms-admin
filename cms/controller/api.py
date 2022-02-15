from flask import Blueprint, jsonify, request
from ..model import Blog, Tag
from ..utils import get_start

api = Blueprint("api", __name__)


@api.get("/")
def index():
    blogs = Blog()
    return jsonify(blogs=blogs.get_all(parse=True))


@api.get("/read/<param>")
def read(param):
    blog = Blog()
    return jsonify(blog.get_one(param))


@api.get("/blogs")
def blogs():
    pages = 1 if not request.args.get("page") else int(request.args.get("page"))
    blog = Blog()
    return jsonify(blogs=blog.get_some(show_hidden=True, offset=get_start(pages)))


@api.get("/t", defaults={"tag": None})
@api.get("/t/<tag>")
def all_tag(tag):
    _tag = Tag()
    pages = None if not request.args.get("page") else int(request.args.get("page"))
    if tag:
        if pages:
            blog = Blog().get_paged_by_tag(tag, page=pages)
            return jsonify(blogs=blog)
        else:
            blog = Blog().get_all_by_tag(tag)
            return jsonify(blogs=blog)
    else:
        if pages:
            return jsonify(tags=_tag.get_paged(pages))
    return jsonify(tags=_tag.get_all())
