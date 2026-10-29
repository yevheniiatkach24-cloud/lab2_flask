from flask import render_template, redirect, url_for, request, session, flash, make_response
from app import app
from app.users import users_bp


@users_bp.route("/")
def hi():
    return render_template("users/hi.html", title="Користувачі")


@users_bp.route("/admin")
def admin():
    return redirect(url_for("users.hi"))


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == "student" and password == "12345":
            session["user"] = username
            flash("Ви успішно увійшли!", "success")
            return redirect(url_for("users.profile"))

        flash("Неправильний логін або пароль.", "danger")

    return render_template("users/login.html", title="Вхід")


@users_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    if request.method == "POST":
        action = request.form.get("action")

        if action == "add":
            name = request.form.get("name", "").strip()
            value = request.form.get("value", "").strip()
            max_age = request.form.get("max_age", "").strip()

            try:
                max_age = int(max_age)

                if not name or max_age <= 0 or name == app.config.get("SESSION_COOKIE_NAME", "session"):
                    raise ValueError

                response = make_response(redirect(url_for("users.profile")))
                response.set_cookie(name, value, max_age=max_age, path="/", httponly=True)
                flash("Cookie успішно додано.", "success")
                return response

            except ValueError:
                flash("Введіть назву та додатний термін дії в секундах.", "danger")

        elif action == "delete":
            name = request.form.get("name", "").strip()
            session_cookie = app.config.get("SESSION_COOKIE_NAME", "session")

            if name and name != session_cookie and name in request.cookies:
                response = make_response(redirect(url_for("users.profile")))
                response.delete_cookie(name, path="/")
                flash("Cookie видалено.", "success")
                return response

            flash("Не вдалося знайти цей cookie.", "warning")

        elif action == "delete_all":
            response = make_response(redirect(url_for("users.profile")))
            session_cookie = app.config.get("SESSION_COOKIE_NAME", "session")

            for name in request.cookies:
                if name != session_cookie:
                    response.delete_cookie(name, path="/")

            flash("Усі cookies, крім cookie сесії, видалено.", "success")
            return response

    theme = request.cookies.get("theme", "light")
    session_cookie = app.config.get("SESSION_COOKIE_NAME", "session")
    cookies = {
        name: value
        for name, value in request.cookies.items()
        if name != session_cookie
    }

    return render_template(
        "users/profile.html",
        title="Профіль",
        username=session["user"],
        theme=theme,
        cookies=cookies
    )


@users_bp.route("/theme/<theme>")
def change_theme(theme):
    if "user" not in session:
        flash("Спочатку увійдіть у систему.", "warning")
        return redirect(url_for("users.login"))

    if theme not in ("light", "dark"):
        flash("Невідома кольорова схема.", "danger")
        return redirect(url_for("users.profile"))

    response = make_response(redirect(url_for("users.profile")))
    response.set_cookie("theme", theme, max_age=60 * 60 * 24 * 365, path="/")
    flash("Кольорову схему змінено.", "success")
    return response


@users_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Ви вийшли із системи.", "info")
    return redirect(url_for("users.login"))