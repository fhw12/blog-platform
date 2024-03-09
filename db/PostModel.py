import sqlite3

class ConnectionHelper:
	def __init__(self):
		self.connection = sqlite3.connect("main.db")
	
	def getConnection(self):
		return self.connection
	
	def close(self):
		self.connection.commit()
		self.connection.close()

	def __del__(self):
		self.close()

class PostModel:
	def __init__(self):
		connection = sqlite3.connect("main.db")
		self.createTable = """
			CREATE TABLE IF NOT EXISTS posts (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				title TEXT,
				content TEXT
			)
		"""

		connection.cursor().execute(self.createTable)
		connection.close()

	def addPost(self, title, content):
		#connection = sqlite3.connect("main.db")
		connectionHelper = ConnectionHelper()
		connectionHelper.getConnection().cursor().execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
		#connection.commit()
		#connection.close()

	def getPosts(self):
		#connection = sqlite3.connect("main.db")
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM posts ORDER BY id DESC")
		ret = cursor.fetchall()
		#connection.close()
		return ret

	def getPostByID(self, postID):
		#connection = sqlite3.connect("main.db")
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM posts WHERE id=?", (postID,))
		ret = cursor.fetchall()
		#connection.close()
		return ret