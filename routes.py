from flask import render_template
from DataBaseController import DBController



class Routes:
	def __init__(self, app):
		self.app = app
		self.dbController = DBController()
		self.create_routes()

	def create_routes(self):
		@self.app.route('/')
		def index():
			return render_template(
				"index.html",
				posts = self.dbController.getPosts(),
			)