
import unittest
from app import app


class TestUserBlueprint(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_users_page(self):
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Вітаю в розділі користувачів!".encode("utf-8"), response.data)

    def test_admin_redirect(self):
        response = self.client.get("/users/admin")
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
