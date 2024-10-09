from flask import Flask

from hashlib import sha256
from flask import render_template, request, session, redirect, url_for
import db.queries as queries

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

if not queries.get_user_by_username("admin"):
    queries.add_user("admin", "adminpassword", "admin")


@app.route("/")
def index():
    posts = queries.get_posts_on_page(page_id=1)
    number_of_pages: int = queries.get_number_of_pages()
    return render_template(
        "index.html", posts=posts, page_id=1, number_of_pages=number_of_pages
    )


@app.route("/<int:page_id>")
def explore(page_id):
    posts = queries.get_posts_on_page(page_id=page_id)
    number_of_pages: int = queries.get_number_of_pages()
    return render_template(
        "index.html", posts=posts, page_id=page_id, number_of_pages=number_of_pages
    )


@app.route("/post/<int:post_id>")
def post(post_id):
    post = queries.get_post_by_id(post_id=post_id)
    post_comments = queries.get_comments_by_post_id(post_id=post_id)
    comments = []
    for comment in post_comments:
        author: str = queries.get_user_by_id(comment.creator_id).username
        comments.append((comment.id, comment.post_id, comment.content, author))
    return render_template("post.html", post=post, comments=comments)


@app.route("/profile")
def profile():
    return render_template("profile.html", error_text="")


@app.route("/auth")
def auth():
    return render_template("auth.html", error_text="")


@app.route("/createAccount")
def createAccount():
    return render_template("createAccount.html", error_text="")


@app.route("/signup", methods=["POST"])
def signup():
    username: str = request.form["username"]
    password: str = request.form["password"]
    repeated_password: str = request.form["repeatpassword"]
    if password != repeated_password:
        return render_template("createAccount.html", error_text="Пароли не совпадают")
    user = queries.get_user_by_username(username=username)
    if user:
        return render_template(
            "createAccount.html", error_text="Пользователь уже существует"
        )
    else:
        queries.add_user(username, password, "user")
        return redirect(url_for("index"))


@app.route("/login", methods=["POST"])
def login():
    username: str = request.form["username"]
    password: str = request.form["password"]
    user = queries.get_user_by_username(username=username)
    if user:
        password_hash: str = sha256(password.encode()).hexdigest()

        if user.password == password_hash:
            session["username"] = username
            session["role"] = user.role
        else:
            return render_template(
                "auth.html",
                error_text="Неверный пароль",
            )
    else:
        return render_template("auth.html", error_text="Неверный логин")
    return redirect(url_for("index"))


@app.route("/changePassword", methods=["POST"])
def changePassword():
    username: str = session["username"]
    password: str = request.form["password"]
    new_password = request.form["newpassword"]
    user = queries.get_user_by_username(username=username)
    if user:
        password_hash: str = sha256(password.encode()).hexdigest()

        if user.password == password_hash:
            queries.set_user_password_by_username(
                username=user.username, new_password=new_password
            )
        else:
            return render_template(
                "profile.html",
                error_text="Неверный текущий пароль",
            )
    return render_template("profile.html", error_text="Пароль успешно обновлен")


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("role", None)
    return redirect(url_for("index"))


@app.route("/newPost")
def newPost():
    return render_template("newPost.html")


@app.route("/sendNewPost", methods=["POST"])
def sendNewPost():
    if session["role"] != "admin":
        return "Доступ запрещен!"
    title: str = request.form["title"]
    content: str = request.form["content"]
    if "username" in session:
        queries.add_post(title=title, content=content)
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route("/sendNewComment/<int:post_id>", methods=["POST"])
def sendNewComment(post_id):
    content: str = request.form["content"]
    if "username" in session:
        user_id: int = queries.get_user_by_username(session["username"]).id
        queries.add_comment(post_id=post_id, content=content, creator_id=user_id)
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route("/deletePost/<int:post_id>")
def deletePost(post_id):
    if "role" in session:
        if session["role"] != "admin":
            return "Доступ запрещен!"
    else:
        return "Доступ запрещен!"
    queries.delete_post_by_id(post_id=post_id)
    return redirect(url_for("index"))


@app.route("/editPost/<int:post_id>")
def editPost(post_id):
    if "role" in session:
        if session["role"] != "admin":
            return "Доступ запрещен!"
    else:
        return "Доступ запрещен!"
    return render_template(
        "editPost.html", post=queries.get_post_by_id(post_id=post_id)
    )


@app.route("/sendEditPost/<int:post_id>", methods=["POST"])
def sendEditPost(post_id):
    if "role" in session:
        if session["role"] != "admin":
            return "Доступ запрещен!"
    else:
        return "Доступ запрещен!"
    title: str = request.form["title"]
    content: str = request.form["content"]
    if "username" in session:
        queries.update_post_by_id(post_id=post_id, title=title, content=content)
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
