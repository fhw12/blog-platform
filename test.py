from flask import session, Flask, request, redirect, url_for
app = Flask(__name__)
# установим секретный ключ для подписи. Держите это в секрете!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return f'Вошел как {session["username"]}'
    return 'Вы не авторизованы'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # устанавливаем сессию для пользователя
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # удаляем имя пользователя из сеанса, если оно есть
    session.pop('username', None)
    return redirect(url_for('index'))

app.run(debug = True)