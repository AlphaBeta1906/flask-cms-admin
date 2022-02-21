from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    current_app,
    make_response
)
from werkzeug.utils import secure_filename

from os import path

from ..model import Blog
from ..utils import is_admin
from ..utils.forms import PostForm

post = Blueprint("post", __name__)


def get_unique_id():
    import random
    import string

    return "".join(random.choices(string.ascii_lowercase + string.digits, k=4))


@post.route("/blogs")
def index():
    blogs = Blog()
    return jsonify(blogs=blogs.get_all())


@post.route("/add_blogs", methods=["GET", "POST"])
@is_admin
def add_blog():
    forms = PostForm()
    if request.method == "POST" and forms.validate_on_submit():
        cover_image = forms.cover_image.data
        filename = None
        if cover_image:
            ext = cover_image.filename.split(".")[-1]
            filename = f"{get_unique_id()}.{ext}"
            cover_image.save(
                path.join(current_app.config["IMAGE_COVER_PATH"], filename)
            )
        print(forms.content.data)
        blog = Blog(
            title=forms.title.data,
            content=forms.content.data,
            hidden=forms.is_hidden.data,
            image=f"img_cover/{filename}" if cover_image else None,
            tag=",".join(forms.tag.data),
            keywords=forms.keywords.data,
        )
        blog.add_blog()
        return redirect(url_for("admin.dashboard"))
    return render_template("post/addpost.jinja", forms=forms)


@post.route("/edit_blog/<int:id>", methods=["GET", "POST"])
@is_admin
def edit_blog(id):
    forms = PostForm()
    blog = Blog().get_one(id, parse=False)
    temp_blog = Blog().get_one(id, parse=False)
    if request.method == "POST" and forms.validate_on_submit():
        cover_image = forms.cover_image.data
        filename = None
        if cover_image:
            filename = f"{get_unique_id()}.{ext}"
            ext = cover_image.filename.split(".")[-1]
            save_image = blog.image.split("/")[1] if blog.image else file
            print(save_image)
            cover_image.save(
                path.join(
                    current_app.config["IMAGE_COVER_PATH"], blog.image.split("/")[1]
                )
                if blog.image
                else filename
            )
        _blog = Blog(
            title=forms.title.data,
            content=forms.content.data,
            hidden=forms.is_hidden.data,
            tag=",".join(forms.tag.data),
            image=None
            if blog.image
            else (f"img_cover/{filename}" if cover_image else None),
            keywords=forms.keywords.data,
        )
        _blog.update_blog(id=blog.id)
        return redirect(url_for("admin.dashboard"))
    forms.title.data = blog.title
    forms.content.data = blog.content
    forms.is_hidden.data = blog.hidden
    forms.tag.data = blog.tag.split(",")
    forms.keywords.data = blog.keywords
    return render_template("post/editpost.jinja", forms=forms, blog=blog)


@post.get("/preview/<int:id>")
@is_admin
def read(id):
    blog = Blog().get_one(id, parse=False)
    return render_template("post/readpost.jinja", blog=blog)


@post.delete("/delete_blog/<int:id>")
@is_admin
def delete_blog(id):
    blog = Blog()
    blog.delete_blog(id)
    return jsonify(message="blog deleted")

@post.post("/upload_image")
@is_admin
def upload_image():
    image = request.files.get("file")
    print(image)
    if image:
        ext = image.filename.split(".")[-1]        
        filename = f"{get_unique_id()}.{ext}"
        if ext in ['jpg', 'gif', 'png', 'jpeg']:
            save_path = path.join(current_app.config["IMAGE_UPLOAD_PATH"],filename)
            image.save(save_path)
            return jsonify(location=f"/static/blog_image/{filename}")
    return jsonify(msg="fail")