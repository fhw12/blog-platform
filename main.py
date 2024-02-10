from flask import Flask

from routes import Routes

class WebApp:
	def __init__(self):
		self.app = Flask(__name__)

		self.routes = Routes(self.app)

		self.app.run(debug = True)

if __name__ == '__main__':
	web_app = WebApp()