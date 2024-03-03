import random

class SessionController:
    def __init__(self):
        self.activeSessions = {}
    
    def addSession(self, username):
        if username in self.activeSessions:
            return None
        
        self.activeSessions[username] = random.randint(0, 2**256)

    def auth(self, username, key):
        if username not in self.activeSessions:
            return False
        
        if self.activeSessions[username] != key:
            return False
        
        return True