
import os
from flask import Flask

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "lab5-development-key-change-before-deployment"
)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

from app import views
from app.users import users_bp
from app.products import products_bp

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
