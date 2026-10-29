from flask import render_template
from app import app


@app.route("/")
@app.route("/resume")
def resume():
    return render_template(
        "resume.html",
        title="Моє резюме",
        name="Євгенія Ткач"
    )


@app.route("/contacts")
def contacts():
    return render_template("contacts.html", title="Контакти")


@app.route("/home")
def homepage():
    return render_template("homepage.html", title="Головна сторінка")