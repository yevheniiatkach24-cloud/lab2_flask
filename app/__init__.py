import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "lab5-development-key-change-before-deployment"
)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db.init_app(app)

migrate = Migrate()
migrate.init_app(app, db)

from app import views
from app.users import users_bp
from app.products import products_bp

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)

from app.posts import posts_bp
app.register_blueprint(posts_bp)