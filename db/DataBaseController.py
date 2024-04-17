import sqlite3

import db.PostModel as PostModel
import db.UserModel as UserModel

class DBController:
	def __init__(self):
		self.postModel = PostModel.PostModel()
		self.userModel = UserModel.UserModel()

	def addPost(self, title, content):
		self.postModel.addPost(title, content)

	def updatePostByID(self, postID, title, content):
		self.postModel.updatePostByID(postID, title, content)

	def deletePostByID(self, postID):
		self.postModel.deletePostByID(postID)

	def getPostById(self, postID):
		return self.postModel.getPostByID(postID)
	
	def getPostsOnPage(self, pageId):
		return self.postModel.getPostsOnPage(pageId)

	def getNumberOfPages(self):
		return self.postModel.getNumberOfPages()

	def getPosts(self):
		return self.postModel.getPosts()

	def getUserByUsername(self, username):
		return self.userModel.getUserByUsername(username)
	
	def addUser(self, username, password):
		self.userModel.addUser(username, password)

