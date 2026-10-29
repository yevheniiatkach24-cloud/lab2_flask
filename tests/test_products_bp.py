
import unittest

from app import app
from app.products import views
from tinydb import TinyDB
from tinydb.storages import MemoryStorage


class TestProductsBlueprint(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False

        self.client = app.test_client()

        # Зберігаємо справжню таблицю товарів
        self.original_table = views.products_table

        # Створюємо тимчасову базу в пам'яті
        self.test_db = TinyDB(storage=MemoryStorage)
        views.products_table = self.test_db.table("products")

        # Додаємо тестовий товар
        views.products_table.insert({
            "id": 1,
            "name": "Тестовий ноутбук",
            "content": "Тестовий опис товару",
            "price": "15000.00",
            "category": "Електроніка",
            "quantity": 5,
            "image": "",
            "created_at": "2026-10-29 12:00:00",
        })

    def tearDown(self):
        # Повертаємо справжню таблицю
        views.products_table = self.original_table

        # Закриваємо тимчасову базу
        self.test_db.close()

    def test_products_list(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Тестовий ноутбук".encode(), response.data)

    def test_product_detail(self):
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Тестовий ноутбук".encode(), response.data)

    def test_product_not_found(self):
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 404)

    def test_product_add_page(self):
        response = self.client.get("/products/add")
        self.assertEqual(response.status_code, 200)

    def test_product_add(self):
        response = self.client.post(
            "/products/add",
            data={
                "name": "Тестова мишка",
                "content": "Комп'ютерна мишка",
                "price": "500.00",
                "category": "Електроніка",
                "quantity": "10",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

        product = views.products_table.get(
            lambda item: item.get("name") == "Тестова мишка"
        )
        self.assertIsNotNone(product)
        self.assertEqual(product["quantity"], 10)

    def test_product_edit_page(self):
        response = self.client.get("/products/1/edit")
        self.assertEqual(response.status_code, 200)

    def test_product_edit(self):
        response = self.client.post(
            "/products/1/edit",
            data={
                "name": "Оновлений ноутбук",
                "content": "Оновлений опис",
                "price": "18000.00",
                "category": "Електроніка",
                "quantity": "3",
            },
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

        product = views.products_table.get(
            lambda item: item.get("id") == 1
        )
        self.assertEqual(product["name"], "Оновлений ноутбук")
        self.assertEqual(product["quantity"], 3)

    def test_product_delete(self):
        response = self.client.post(
            "/products/1/delete",
            follow_redirects=True,
        )

        self.assertEqual(response.status_code, 200)

        product = views.products_table.get(
            lambda item: item.get("id") == 1
        )
        self.assertIsNone(product)

    def test_product_delete_not_found(self):
        response = self.client.post("/products/999/delete")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
