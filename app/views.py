
import logging

from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import ContactForm


logging.basicConfig(
    filename="contact.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


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


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        try:
            logging.info(
                "Контактна форма: name=%s, email=%s, subject=%s, message=%s",
                form.name.data,
                form.email.data,
                form.subject.data,
                form.message.data
            )
            flash("Повідомлення успішно надіслано!", "success")
        except Exception:
            logging.exception("Помилка запису контактної форми")
            flash("Не вдалося зберегти повідомлення.", "danger")

        return redirect(url_for("contact"))

    return render_template(
        "contact.html",
        title="Контактна форма",
        form=form
    )
