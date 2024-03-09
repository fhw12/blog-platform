import sqlite3
from db.ConnectionHelper import ConnectionHelper

class UserModel:
	def __init__(self):
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		self.createTable = """
			CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				username TEXT,
				password TEXT
			)
		"""

		connection.cursor().execute(self.createTable)

	def addUser(self, username, password):
		connectionHelper = ConnectionHelper()
		connectionHelper.getConnection().cursor().execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

	def getUsers(self):
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM users ORDER BY id DESC")
		ret = cursor.fetchall()
		return ret

	def getUserByID(self, userID):
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM users WHERE id=?", (userID,))
		ret = cursor.fetchall()
		return ret

	def getUserByUsername(self, username):
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM users WHERE username=?", (username,))
		ret = cursor.fetchall()
		return ret
