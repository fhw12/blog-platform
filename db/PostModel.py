import sqlite3
from db.ConnectionHelper import ConnectionHelper

class PostModel:
	def __init__(self):
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		self.createTable = """
			CREATE TABLE IF NOT EXISTS posts (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				title TEXT,
				content TEXT
			)
		"""
		connection.cursor().execute(self.createTable)

	def addPost(self, title, content):
		connectionHelper = ConnectionHelper()
		connectionHelper.getConnection().cursor().execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))

	def getPosts(self):
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM posts ORDER BY id DESC")
		ret = cursor.fetchall()
		return ret

	def getPostByID(self, postID):
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM posts WHERE id=?", (postID,))
		ret = cursor.fetchall()
		return ret
	
	def deletePostByID(self, postID):
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		cursor = connection.cursor()
		cursor.execute("DELETE FROM posts WHERE id=?", (postID,))

	def updatePostByID(self, postID, title, content):
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		cursor = connection.cursor()
		cursor.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, postID,))