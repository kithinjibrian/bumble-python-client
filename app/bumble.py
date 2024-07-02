from proto_py import user_pb2
from request.request import Request

from sraso.load import ( load )
from db_objects.dbo import ( Compose )

class Bumble:
    def __init__(self, config_filepath):
        self.config_filepath = config_filepath
        self.config = None
        self.retries = 0
        self.read_config()
    
    def read_config(self):
        try:
            with open(self.config_filepath, 'r') as file:
                self.config = load(file.read())
        except FileNotFoundError:
            raise Exception("config file not found")
            
    def pack_user(self):
        user = user_pb2.user_transit_proto()
        user.username = self.config['user']['username']
        user.password = self.config['user']['password']
        return user.SerializeToString()
    
    def uae(self, action):
        uae = self.config['connection']
        uae["action"] = action
        return uae
    
    def register(self):
        prot = Request(self.uae("user-register"), self.pack_user()).send()
        return prot.body.decode("utf-8")
            
    def login(self):        
        log = Request(self.uae("user-login"), self.pack_user()).send()
        
        if log.status == 401:
            raise Exception("invalid credentials")
        
        with open("token", 'wb') as file:
            file.write(log.body)
        return log
    
    def read_token(self):
        token = None
        try:
            with open("token", 'rb') as file:
                token = file.read()
        except FileNotFoundError:
            token = self.login().body
        return token
        
    def save(self, key, value):
        obj = Compose(key, value)
        prot = Request(self.uae("cache-save"), str(obj).encode("utf-8"), self.read_token()).send()
        
        if self.retries > 1:
            raise Exception("too many retries trying to save value")
        
        if prot.status == 401:
            self.login()
            self.retries += 1
            return self.save(key, value)
            
        self.retries = 0
            
        return prot.body.decode("utf-8")
            
    def get(self, key):
        prot = Request(self.uae("cache-get"), key.encode("utf-8"), self.read_token()).send()
        
        if self.retries > 1:
            raise Exception("too many retries trying to get value")
        
        if prot.status == 401:
            self.login()
            self.retries += 1
            return self.get(key)
            
        self.retries = 0
        return load(prot.body.decode("utf-8"))