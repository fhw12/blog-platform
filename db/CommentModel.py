import sqlite3
from db.ConnectionHelper import ConnectionHelper

class CommentModel:
	def __init__(self):
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		self.createTable = """
			CREATE TABLE IF NOT EXISTS comments (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				postId int,
				content TEXT,
                creatorId int
			)
		"""
		connection.cursor().execute(self.createTable)

	def addComment(self, postId, content, creatorId):
		connectionHelper = ConnectionHelper()
		connectionHelper.getConnection().cursor().execute("INSERT INTO comments (postId, content, creatorId) VALUES (?, ?, ?)", (postId, content, creatorId))

	def getCommentsByPostId(self, postId):
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM comments WHERE postId=? ORDER BY id DESC", (postId,))
		ret = cursor.fetchall()
		return ret

	# def getPostByID(self, postID):
	# 	connectionHelper = ConnectionHelper()
	# 	connection = connectionHelper.getConnection()
	# 	cursor = connection.cursor()
	# 	cursor.execute("SELECT * FROM posts WHERE id=?", (postID,))
	# 	ret = cursor.fetchall()
	# 	return ret
	
	def deleteCommentById(self, postID):
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		cursor = connection.cursor()
		cursor.execute("DELETE FROM comments WHERE id=?", (postID,))

	# def updatePostByID(self, postID, title, content):
	# 	connectionHelper = ConnectionHelper()
	# 	connection = connectionHelper.getConnection()
	# 	cursor = connection.cursor()
	# 	cursor.execute("UPDATE posts SET title=?, content=? WHERE id=?", (title, content, postID,))