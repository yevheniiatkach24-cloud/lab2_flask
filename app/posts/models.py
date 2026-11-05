from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    author = db.Column(db.String(20), default="Anonymous")

    def __repr__(self):
        return f"<Post {self.title}>"
