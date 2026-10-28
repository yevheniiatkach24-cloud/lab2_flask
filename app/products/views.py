
from flask import render_template
from app.products import products_bp


products = [
    {"id": 1, "name": "Ноутбук", "price": 25000},
    {"id": 2, "name": "Смартфон", "price": 15000},
    {"id": 3, "name": "Навушники", "price": 2000},
]


@products_bp.route("/")
def product_list():
    return render_template(
        "products/list.html",
        title="Список товарів",
        products=products
    )


@products_bp.route("/<int:product_id>")
def product_detail(product_id):
    product = next(
        (item for item in products if item["id"] == product_id),
        None
    )

    if product is None:
        return "Товар не знайдено", 404

    return render_template(
        "products/detail.html",
        title=product["name"],
        product=product
    )
