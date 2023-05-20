import redis
from redis import Redis

class Redi(Redis):
    def __init__(self, host, port, db):
        super().__init__(host=host, port=port, db=db)
        
    def exist(self, key):
        try:
            return self.exists(key)
        except:
            return False
        
    def value(self, key):
        try:
            return self.get(key)
        except:
            return None
        
    def get(self, key):
        try:
            return super().get(key)
        except:
            return None