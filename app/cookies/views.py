from flask import render_template, request, redirect, url_for, make_response
from app.cookies import cookies_bp


@cookies_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            name = request.form.get("name", "").strip()
            value = request.form.get("value", "").strip()

            if name:
                response = make_response(redirect(url_for("cookies.index")))
                response.set_cookie(name, value, max_age=60 * 60 * 24 * 7)
                return response

        elif action == "delete":
            name = request.form.get("name", "").strip()

            if name:
                response = make_response(redirect(url_for("cookies.index")))
                response.delete_cookie(name)
                return response

    return render_template("cookies/index.html", title="Робота з cookies")