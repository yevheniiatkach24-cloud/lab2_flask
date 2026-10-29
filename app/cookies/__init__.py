from flask import Blueprint

cookies_bp = Blueprint("cookies", __name__, url_prefix="/cookies")

from app.cookies import views