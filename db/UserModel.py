import sqlite3
import hashlib
from db.ConnectionHelper import ConnectionHelper

class UserModel:
	def __init__(self):
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		self.createTable = """
			CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				username TEXT,
				password TEXT,
				role TEXT
			)
		"""

		connection.cursor().execute(self.createTable)

		if len(self.getUserByUsername('admin')) == 0:
			self.addUser("admin", "1234", "admin")

	def addUser(self, username, password, role):
		hashOfpassword = hashlib.sha256(password.encode()).hexdigest()
		connectionHelper = ConnectionHelper()
		connectionHelper.getConnection().cursor().execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashOfpassword, role))

	def getUsers(self):
		connectionHelper = ConnectionHelper()
		connection = connectionHelper.getConnection()
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM users ORDER BY id DESC")
		ret = cursor.fetchall()
		return ret

	def getUserById(self, userID):
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
