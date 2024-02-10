import sqlite3

import PostModel

class DBController:
	def __init__(self):
		#pass
		#self.connection = sqlite3.connect("main.db")
		self.postModel = PostModel.PostModel()

	def addPosts(self, title, content):
		self.postModel.addPost(title, content)

	def getPostById(self, postID):
		return self.postModel.getPostByID(postID)

	def getPosts(self):
		return self.postModel.getPosts()

# dbController = DBController()

# for post in dbController.getPosts():
# 	print(post)