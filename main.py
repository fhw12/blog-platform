from flask import Flask
import flask_login
import os

from routes import Routes

class WebApp:
	def __init__(self):
		self.app = Flask(__name__)
		self.app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
		self.routes = Routes(self.app)
		self.app.run(debug = True, host="0.0.0.0")

if __name__ == '__main__':
	web_app = WebApp()