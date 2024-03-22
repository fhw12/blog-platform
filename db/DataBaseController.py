import sqlite3

import db.PostModel as PostModel
import db.UserModel as UserModel

class DBController:
	def __init__(self):
		self.postModel = PostModel.PostModel()
		self.userModel = UserModel.UserModel()

	def addPost(self, title, content):
		self.postModel.addPost(title, content)

	def getPostById(self, postID):
		return self.postModel.getPostByID(postID)

	def getPosts(self):
		return self.postModel.getPosts()

	def getUserByUsername(self, username):
		return self.userModel.getUserByUsername(username)
	
	def addUser(self, username, password):
		self.userModel.addUser(username, password)

