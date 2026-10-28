
from flask import render_template, redirect, url_for
from app.users import users_bp


@users_bp.route("/")
def hi():
    return render_template("users/hi.html", title="Користувачі")


@users_bp.route("/admin")
def admin():
    return redirect(url_for("users.hi"))
