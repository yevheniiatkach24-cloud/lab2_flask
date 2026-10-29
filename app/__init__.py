from flask import Flask

app = Flask(__name__)
app.config["SECRET_KEY"] = "lab4-secret-key-change-later"

from app import views
from app.users import users_bp
from app.products import products_bp
from app.cookies import cookies_bp

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(cookies_bp)