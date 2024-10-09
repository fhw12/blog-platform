from flask import Flask
import flask_login
import os

import hashlib
from flask import render_template, request, session, redirect, url_for
import db.queries as queries

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

if not queries.get_user_by_username('admin'):
    queries.add_user('admin', 'adminpassword', 'admin')

@app.route('/')
def index():
    posts = queries.get_posts_on_page(page_id=1)
    numberOfpages = queries.get_number_of_pages()
    return render_template(
        'index.html',
        posts = posts,
        pageId = 1,
        numberOfpages = numberOfpages
    )

@app.route('/<int:pageId>')
def explore(pageId):
    posts = queries.get_posts_on_page(page_id=pageId)
    numberOfpages = queries.get_number_of_pages()
    return render_template(
        'index.html',
        posts = posts,
        pageId = pageId,
        numberOfpages = numberOfpages
    )


@app.route('/post/<int:postId>')
def post(postId):
    post = queries.get_post_by_id(post_id=postId)
    postComments = queries.get_comments_by_post_id(post_id=postId)
    comments = []
    for item in postComments:
        author = queries.get_user_by_id(item.creator_id).username
        comments.append((item.id, item.post_id, item.content, author))
    return render_template(
        'post.html',
        post = post,
        comments = comments
    )

@app.route('/profile')
def profile():
    return render_template(
        'profile.html',
        errorText = ''
    )

@app.route('/auth')
def auth():
    return render_template(
        'auth.html',
        errorText = ''
    )

@app.route('/createAccount')
def createAccount():
    return render_template(
        'createAccount.html',
        errorText = ''
    )

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    repeatpassword = request.form['repeatpassword']
    if password != repeatpassword:
        return render_template(
            'createAccount.html',
            errorText = "Пароли не совпадают"
        )
    user = queries.get_user_by_username(username=username)
    if user:
        return render_template(
            'createAccount.html',
            errorText = 'Пользователь уже существует'
        )
    else:
        queries.add_user(username, password, "user")
        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = queries.get_user_by_username(username=username)
    if user:
        hashOfpassword = hashlib.sha256(password.encode()).hexdigest()

        if user.password == hashOfpassword:
            session['username'] = username
            session['role'] = user.role
        else:
            return render_template(
                'auth.html',
                errorText = "Неверный пароль",
            )
    else:
        return render_template(
                "auth.html",
                errorText = "Неверный логин"
            )
    return redirect(url_for('index'))

@app.route('/changePassword', methods=['POST'])
def changePassword():
    username = session['username']
    password = request.form['password']
    newPassword = request.form['newpassword']
    user = queries.get_user_by_username(username=username)
    if user:
        hashOfpassword = hashlib.sha256(password.encode()).hexdigest()

        if user.password == hashOfpassword:
            queries.set_user_password_by_username(username=user.username, new_password=newPassword)
        else:
            return render_template(
                'profile.html',
                errorText = "Неверный текущий пароль",
            )
    return render_template(
        'profile.html',
        errorText = "Пароль успешно обновлен"
    )

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))

@app.route('/newPost')
def newPost():
    return render_template(
        'newPost.html'
    )

@app.route('/sendNewPost', methods=['POST'])
def sendNewPost():
    if session['role'] != 'admin':
        return "Доступ запрещен!"
    title = request.form['title']
    content = request.form['content']
    if 'username' in session:
        queries.add_post(title=title, content=content)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/sendNewComment/<int:postId>', methods=['POST'])
def sendNewComment(postId):
    content = request.form['content']
    if 'username' in session:
        userId = queries.get_user_by_username(session['username']).id
        queries.add_comment(post_id=postId, content=content, creator_id=userId)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/deletePost/<int:postId>')
def deletePost(postId):
    if 'role' in session:
        if session['role'] != 'admin':
            return "Доступ запрещен!"
    else:
        return "Доступ запрещен!"
    queries.delete_post_by_id(post_id=postId)
    return redirect(url_for('index'))

@app.route('/editPost/<int:postId>')
def editPost(postId):
    if 'role' in session:
        if session['role'] != 'admin':
            return "Доступ запрещен!"
    else:
        return "Доступ запрещен!"
    return render_template(
        'editPost.html',
        post = queries.get_post_by_id(post_id=postId)
    )

@app.route('/sendEditPost/<int:postId>', methods=['POST'])
def sendEditPost(postId):
    if 'role' in session:
        if session['role'] != 'admin':
            return "Доступ запрещен!"
    else:
        return "Доступ запрещен!"
    title = request.form['title']
    content = request.form['content']
    if 'username' in session:
        queries.update_post_by_id(post_id=postId, title=title, content=content)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0")