from flask import current_app, abort
from werkzeug.security import generate_password_hash
from flask_login import UserMixin, current_user
from sqlalchemy.sql import func
from os import path, remove
from . import app, db, marshmallow
from .utils import get_start


class BlogSchema(marshmallow.Schema):
    class Meta:
        fields = ("id", "author", "title", "content", "tag", "slug", "date")


class TagSchema(marshmallow.Schema):
    class Meta:
        fields = ("id", "tag", "description")


class BaseId:
    """by default all table have this is field"""

    id = db.Column(db.Integer, primary_key=True)


class Admin(db.Model, UserMixin, BaseId):
    username = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(2000), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    profile_picture = db.Column(db.String(500), nullable=True)
    role = db.Column(db.String(24), default="admin")

    def __init__(self, username=None, password=None, email=None):
        self.username = username
        self.password = password
        self.email = email

    def add_admin(self):
        with app.app_context():
            self.password = generate_password_hash(self.password, method="SHA512")
            db.session.add(self)
            db.session.commit()

    def select_by_username(self):
        return self.query.filter_by(username=self.username).first()


class Blog(db.Model, BaseId):
    author = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.String(10000), nullable=False)
    slug = db.Column(db.String(2000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    hidden = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(200))
    tag = db.Column(db.String(1000), nullable=False)
    keywords = db.Column(db.String(1000))

    blogs_schema = BlogSchema(many=True)
    blog_schema = BlogSchema()

    def __init__(
        self, title=None, content=None, hidden=None, image=None, tag=None, keywords=None
    ):
        self.author = current_user.username if current_user.is_authenticated else None
        self.title = title
        self.content = content
        self.slug = title.replace(" ", "-") if title else title
        self.hidden = hidden
        self.image = image
        self.tag = tag
        self.keywords = keywords

    def add_blog(self):
        db.session.add(self)
        db.session.commit()

    def update_blog(self, id):
        update = self.query.filter_by(id=id).first()
        update.title = self.title if self.title else update.title
        update.content = self.content if self.content else update.title
        update.slug = update.title.replace(" ", ",")
        update.image = self.image if self.image else update.image
        update.tag = self.tag if self.tag else update.tag
        update.hidden = self.hidden if self.hidden else update.hidden
        update.keyword = self.keywords if self.keywords else update.tag
        db.session.commit()

    def delete_blog(self, id):
        delete = self.query.filter_by(id=id).first_or_404()
        if delete.image:
            remove(
                path.join(
                    current_app.config["IMAGE_COVER_PATH"], delete.image.split("/")[1]
                )
            )
        db.session.delete(delete)
        db.session.commit()

    def get_all(self, parse=True, show_hidden=False):
        _all = (
            self.query.filter_by(hidden=False).all()
            if not show_hidden
            else self.query.all()
        )
        if not parse:
            return _all
        return self.blogs_schema.dump(_all)

    def get_one(self, param, parse=True):
        blog = None
        if isinstance(param, int) or param.isnumeric():
            id = int(param)
            blog = self.query.filter_by(id=id).first_or_404()
        else:
            blog = self.query.filter_by(slug=param).first_or_404()

        if not parse:
            return blog
        return self.blog_schema.dump(blog)

    def get_some(self, limit=5, offset=0, show_hidden=False):
        blogs = self.query.filter_by(hidden=False).offset(offset).limit(limit).all()
        if show_hidden:
            blogs = self.query.offset(offset).limit(limit).all()
        return self.blogs_schema.dump(blogs)

    def get_all_by_tag(self, tag, show_hidden=False, parse=True):
        _all = None
        if show_hidden:
            _all = self.query.filter_by(tag=tag).all()
        else:
            _all = self.query.filter_by(tag=tag, hidden=show_hidden).all()

        if len(_all) <= 0:
            abort(404)
        if parse:
            return self.blogs_schema.dump(_all)
        return _all

    def get_paged_by_tag(self, tag, page, show_hidden=False):
        blogs = (
            self.query.filter_by(hidden=False, tag=tag)
            .offset(get_start(page))
            .limit(10)
            .all()
        )
        if show_hidden:
            blogs = (
                self.query.filter_by(tag=tag).offset(get_start(page)).limit(10).all()
            )

        if len(blogs) <= 0:
            abort(404)
        return self.blogs_schema.dump(blogs)


class Tag(db.Model, BaseId):
    tag = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(250), nullable=False)

    tags_schema = TagSchema(many=True)
    tag_schema = TagSchema()

    def __init__(self, tag=None, description=None):
        self.tag = tag
        self.description = description

    def add_tag(self):
        db.session.add(self)
        db.session.commit()

    def update_tag(self, id):
        update = self.query.filter_by(id=id).first_or_404()
        update.tag = self.tag if self.tag else update.tag
        update.description = (
            self.description if self.description else update.description
        )
        db.session.commit()

    def delete_tag(self, id):
        delete = self.query.filter_by(id=id).first_or_404()
        db.session.delete(delete)
        db.session.commit()

    def get_all(self, parse=True):
        _all = self.query.all()
        if parse:
            return self.tags_schema.dump(_all)
        return _all

    def get_one(self, id):
        tag = self.query.filter_by(id=id).first_or_404()
        return tag

    def get_paged(self, page=None):
        if not page:
            return self.get_all()

        tag = self.query.offset(get_start(page)).limit(10).all()
        return self.tags_schema.dump(tag)
