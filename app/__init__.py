from flask import Flask

app = Flask(__name__)

from app import views
from app.users import users_bp
from app.products import products_bp

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)