from flask import Blueprint, render_template, abort, request, redirect, url_for, jsonify
from flask_login import login_required, current_user

from ..utils import is_admin
from ..utils.forms import TagForm
from ..model import Blog, Tag

admin = Blueprint("admin", __name__)


@admin.route("/dashboard", methods=["GET", "POST"])
@is_admin
def dashboard():
    forms = TagForm(request.form)
    tags = Tag().get_all(parse=False)
    test = [tag.tag for tag in tags]
    print(test)
    blogs = Blog().get_all(parse=False, show_hidden=True)
    if request.method == "POST" and forms.validate_on_submit():
        tag = Tag(tag=forms.tag.data, description=forms.description.data)
        tag.add_tag()
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/admin.jinja", blogs=blogs, forms=forms, tags=tags)


@admin.delete("/delete_tag/<int:id>")
def delete_tag(id):
    tags = Tag()
    tags.delete_tag(id)
    return jsonify(msg="tag deleted")


@admin.route("/update_tag/<int:id>", methods=["GET", "POST"])
def update_tag(id):
    forms = TagForm(request.form)
    tag = Tag().get_one(id)
    if request.method == "POST" and forms.validate_on_submit():
        print(forms.tag.data)
        tag = Tag(tag=forms.tag.data, description=forms.description.data)
        tag.update_tag(id)
        return redirect(url_for("admin.dashboard"))
    forms.tag.data = tag.tag
    forms.description.data = tag.description
    return render_template("admin/updatetag.jinja", forms=forms, tag=tag)
