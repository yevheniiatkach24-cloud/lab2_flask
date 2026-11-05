from flask import render_template, request, redirect, url_for, abort, flash
from app.posts import posts_bp
from app.posts.models import Post
from app import db


@posts_bp.route("/", methods=["GET"])
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    return render_template("posts/index.html", posts=posts)


@posts_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        author = request.form.get("author", "").strip() or "Anonymous"

        if not title or not content:
            flash("Заповніть назву та текст публікації.")
            return render_template("posts/form.html", post=None)

        post = Post(title=title, content=content, author=author)
        db.session.add(post)
        db.session.commit()

        flash("Публікацію успішно створено.")
        return redirect(url_for("posts.index"))

    return render_template("posts/form.html", post=None)


@posts_bp.route("/<int:id>", methods=["GET"])
def detail(id):
    post = db.session.get(Post, id)

    if post is None:
        abort(404)

    return render_template("posts/detail.html", post=post)


@posts_bp.route("/<int:id>/update", methods=["GET", "POST"])
def update(id):
    post = db.session.get(Post, id)

    if post is None:
        abort(404)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()
        author = request.form.get("author", "").strip() or "Anonymous"

        if not title or not content:
            flash("Заповніть назву та текст публікації.")
            return render_template("posts/form.html", post=post)

        post.title = title
        post.content = content
        post.author = author

        db.session.commit()

        flash("Публікацію успішно оновлено.")
        return redirect(url_for("posts.detail", id=post.id))

    return render_template("posts/form.html", post=post)


@posts_bp.route("/<int:id>/delete", methods=["POST"])
def delete(id):
    post = db.session.get(Post, id)

    if post is None:
        abort(404)

    db.session.delete(post)
    db.session.commit()

    flash("Публікацію видалено.")
    return redirect(url_for("posts.index"))
