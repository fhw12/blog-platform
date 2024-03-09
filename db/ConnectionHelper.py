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