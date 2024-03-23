from flask import render_template, request, session, redirect, url_for
from db.DataBaseController import DBController

class Routes:
	def __init__(self, app):
		self.app = app
		self.dbController = DBController()
		#self.sessionController = SessionController()
		self.create_routes()

	def create_routes(self):
		@self.app.route('/')
		def index():
			return render_template(
				'index.html',
				posts = self.dbController.getPosts(),
			)

		@self.app.route('/post/<int:post_id>')
		def post(post_id):
			return render_template(
				'post.html',
				post = self.dbController.getPostById(int(post_id))[0]
			)
		
		@self.app.route('/profile')
		def profile():
			return render_template(
				'profile.html'
			)

		@self.app.route('/auth')
		def auth():
			return render_template(
				'auth.html'
			)
		
		@self.app.route('/createAccount')
		def createAccount():
			return render_template(
				'createAccount.html'
			)

		@self.app.route('/signup', methods=['POST'])
		def signup():
			username = request.form['username']
			password = request.form['password']
			repeatpassword = request.form['repeatpassword']

			if password != repeatpassword:
				return "Password and repeat password are not equal!"

			user = self.dbController.getUserByUsername(username)
			if user:
				return "User exists"
			else:
				self.dbController.addUser(username, password)
				return "Your account has been created!"

		@self.app.route('/login', methods=['POST'])
		def login():
			username = request.form['username']
			password = request.form['password']

			user = self.dbController.getUserByUsername(username)

			if user:
				if user[0][2] == password:
					session['username'] = username
				else:
					return "Неверный пароль"
			else:
				return "Неверный логин"

			return redirect(url_for('index'))

		@self.app.route('/logout')
		def logout():
			session.pop('username', None)
			return redirect(url_for('index'))

		@self.app.route('/newPost')
		def newPost():
			return render_template(
				'newPost.html'
			)

		@self.app.route('/sendNewPost', methods=['POST'])
		def sendNewPost():
			title = request.form['title']
			content = request.form['content']

			if 'username' in session:
				self.dbController.addPost(title, content)
				return redirect(url_for('index'))
			else:
				return redirect(url_for('index'))