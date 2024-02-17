from flask import render_template, request
from DataBaseController import DBController

class Routes:
	def __init__(self, app):
		self.app = app
		self.dbController = DBController()
		self.create_routes()

		#self.dbController.addPost("Something new", "Test text")

	def create_routes(self):
		@self.app.route('/')
		def index():
			return render_template(
				"index.html",
				posts = self.dbController.getPosts(),
			)

		@self.app.route('/post/<int:post_id>')
		def post(post_id):
			return render_template(
				"post.html",
				post = self.dbController.getPostById(int(post_id))[0]
			)

		@self.app.route('/auth')
		def auth():
			return render_template(
				"auth.html"
			)

		@self.app.route('/login', methods=['POST'])
		def login():
			username = request.form['username']
			password = request.form['password']
			return f"{username} | {password}"