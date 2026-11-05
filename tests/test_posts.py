import unittest
from app import app, db
from app.posts.models import Post


class TestPosts(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

        with app.app_context():
            db.drop_all()
            db.create_all()

        self.client = app.test_client()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        response = self.client.post("/post/create", data={
            "title": "Тестова публікація",
            "content": "Текст публікації",
            "author": "Євгенія"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Тестова публікація".encode("utf-8"), response.data)

    def test_posts_list(self):
        with app.app_context():
            post = Post(
                title="Публікація для списку",
                content="Текст",
                author="Євгенія"
            )
            db.session.add(post)
            db.session.commit()

        response = self.client.get("/post/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Публікація для списку".encode("utf-8"), response.data)

    def test_post_detail(self):
        with app.app_context():
            post = Post(title="Деталі", content="Текст")
            db.session.add(post)
            db.session.commit()
            post_id = post.id

        response = self.client.get(f"/post/{post_id}")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Деталі".encode("utf-8"), response.data)

    def test_update_post(self):
        with app.app_context():
            post = Post(title="Стара назва", content="Старий текст")
            db.session.add(post)
            db.session.commit()
            post_id = post.id

        response = self.client.post(
            f"/post/{post_id}/update",
            data={
                "title": "Нова назва",
                "content": "Новий текст",
                "author": "Євгенія"
            },
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Нова назва".encode("utf-8"), response.data)

    def test_delete_post(self):
        with app.app_context():
            post = Post(title="Для видалення", content="Текст")
            db.session.add(post)
            db.session.commit()
            post_id = post.id

        response = self.client.post(
            f"/post/{post_id}/delete",
            follow_redirects=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("Для видалення".encode("utf-8"), response.data)

    def test_post_not_found(self):
        response = self.client.get("/post/9999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
