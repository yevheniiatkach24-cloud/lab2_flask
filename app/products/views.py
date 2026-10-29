
import os
from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
)
from tinydb import TinyDB
from werkzeug.utils import secure_filename

from app.products import products_bp
from app.products.forms import ProductForm


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(__file__), "static", "uploads"
)

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = TinyDB(os.path.join(DATA_DIR, "products.json"))
products_table = db.table("products")

MAX_IMAGE_SIZE = 5 * 1024 * 1024


def get_product(product_id):
    return products_table.get(
        lambda item: item.get("id") == product_id
    )


def get_next_id():
    products = products_table.all()
    return max(
        (item.get("id", 0) for item in products),
        default=0
    ) + 1


def save_image(file):
    if not file or not file.filename:
        return None

    filename_original = secure_filename(file.filename)

    original_name = file.filename.strip()

    if "." not in original_name:
        raise ValueError(
            "Файл повинен мати розширення PNG, JPG або JPEG."
        )

    extension = filename_original.rsplit(".", 1)[-1].lower()

    if extension not in {"png", "jpg", "jpeg"}:
        raise ValueError(
            "Дозволені лише зображення PNG, JPG та JPEG."
        )

    file.stream.seek(0, os.SEEK_END)
    size = file.stream.tell()
    file.stream.seek(0)

    if size > MAX_IMAGE_SIZE:
        raise ValueError(
            "Розмір зображення не повинен перевищувати 5 МБ."
        )

    filename = f"{uuid4().hex}.{extension}"
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    return f"uploads/{filename}"


def delete_image(image_path):
    if not image_path:
        return

    filename = os.path.basename(image_path)

    if image_path.startswith("images/"):
        folder = os.path.join(
            os.path.dirname(__file__), "static", "images"
        )
    else:
        folder = UPLOAD_FOLDER

    full_path = os.path.join(folder, filename)

    if os.path.isfile(full_path):
        os.remove(full_path)


def render_product_form(title, form, action, product=None):
    return render_template(
        "products/form.html",
        title=title,
        form=form,
        action=action,
        product=product,
    )


@products_bp.route("/")
def product_list():
    products = products_table.all()

    return render_template(
        "products/list.html",
        title="Список товарів",
        products=products,
    )


@products_bp.route("/<int:product_id>")
def product_detail(product_id):
    product = get_product(product_id)

    if product is None:
        abort(404)

    return render_template(
        "products/detail.html",
        title=product["name"],
        product=product,
    )


@products_bp.route("/add", methods=["GET", "POST"])
def product_add():
    form = ProductForm()

    if form.validate_on_submit():
        try:
            image_path = save_image(form.image.data)

            product = {
                "id": get_next_id(),
                "name": form.name.data.strip(),
                "content": form.content.data.strip(),
                "price": str(form.price.data),
                "category": form.category.data,
                "quantity": form.quantity.data,
                "image": image_path or "",
                "created_at": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }

            products_table.insert(product)

            flash("Товар успішно додано!", "success")

            return redirect(
                url_for("products.product_list")
            )

        except ValueError as error:
            flash(str(error), "danger")

    return render_product_form(
        "Додати товар",
        form,
        "Додати",
    )


@products_bp.route(
    "/<int:product_id>/edit",
    methods=["GET", "POST"],
)
def product_edit(product_id):
    product = get_product(product_id)

    if product is None:
        abort(404)

    form = ProductForm()

    if request.method == "GET":
        form.name.data = product.get("name", "")
        form.content.data = product.get("content", "")
        form.price.data = Decimal(
            str(product.get("price", "0"))
        )
        form.category.data = product.get("category", "Інше")
        form.quantity.data = product.get("quantity", 0)

    if form.validate_on_submit():
        try:
            uploaded_file = form.image.data
            new_image_path = None

            # Зберігаємо нове фото, якщо файл вибрано.
            if uploaded_file and uploaded_file.filename:
                new_image_path = save_image(uploaded_file)

            old_image_path = product.get("image", "")

            product.update({
                "name": form.name.data.strip(),
                "content": form.content.data.strip(),
                "price": str(form.price.data),
                "category": form.category.data,
                "quantity": form.quantity.data,
            })

            # Якщо нове фото не вибрано, старе залишається.
            if new_image_path:
                product["image"] = new_image_path

            products_table.update(
                product,
                lambda item: item.get("id") == product_id,
            )

            # Видаляємо старе фото після заміни.
            if new_image_path:
                delete_image(old_image_path)

            flash(
                "Зміни успішно збережено!",
                "success",
            )

            return redirect(
                url_for(
                    "products.product_detail",
                    product_id=product_id,
                )
            )

        except ValueError as error:
            flash(str(error), "danger")

    return render_product_form(
        "Редагувати товар",
        form,
        "Зберегти",
        product=product,
    )


@products_bp.route(
    "/<int:product_id>/delete",
    methods=["POST"],
)
def product_delete(product_id):
    product = get_product(product_id)

    if product is None:
        abort(404)

    delete_image(product.get("image", ""))

    products_table.remove(
        lambda item: item.get("id") == product_id
    )

    flash("Товар видалено.", "success")

    return redirect(
        url_for("products.product_list")
    )
