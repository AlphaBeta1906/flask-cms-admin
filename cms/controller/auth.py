from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash

from ..utils import forms
from ..model import Admin

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if "logged" in session:
        return redirect(url_for("admin.dashboard"))

    _forms = forms.Login(request.form)
    if request.method == "POST" and _forms.validate_on_submit():
        username = _forms.username.data
        password = _forms.password.data
        admin = Admin(username, password)
        admin = admin.select_by_username()
        if admin:
            if check_password_hash(admin.password, password):
                login_user(admin)
                session["logged"] = True
                return redirect(url_for("admin.dashboard"))
            else:
                flash("invalid user", category="danger")
                return redirect(url_for("auth.login"))
        else:
            flash("user not exists", category="danger")
            return redirect(url_for("auth.login"))

    return render_template("auth/login.jinja", forms=_forms)


@auth.get("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("auth.login"))
