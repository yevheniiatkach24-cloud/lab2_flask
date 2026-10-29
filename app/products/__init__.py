from flask import Blueprint

products_bp = Blueprint(
    "products",
    __name__,
    url_prefix="/products",
    static_folder="static",
    static_url_path="/static"
)

from app.products import views