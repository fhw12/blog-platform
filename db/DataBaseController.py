import sqlite3

import db.PostModel as PostModel

class DBController:
	def __init__(self):
		self.postModel = PostModel.PostModel()

	def addPost(self, title, content):
		self.postModel.addPost(title, content)

	def getPostById(self, postID):
		return self.postModel.getPostByID(postID)

	def getPosts(self):
		return self.postModel.getPosts()

# dbController = DBController()

# for post in dbController.getPosts():
# 	print(post)