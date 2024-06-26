import time
import json
import socket
import pysodium
from db_objects.dbo import (
    Compose
)
from sraso import load
from proto_py import bee_pb2, user_pb2, bumble_pb2


def serialize_request(action, is_enc, nonce, body):
    bumble = bumble_pb2.request_proto()
    bumble.action = action
    bumble.is_enc = is_enc
    bumble.nonce = nonce
    bumble.body = body
    return bumble.SerializeToString()

def unserialize_response(response):
    res = bumble_pb2.response_proto()
    res.ParseFromString(response)
    return res

def unserialize_response_enc(res, shared_key):
    res = unserialize_response(res)
    if(res.is_enc):
        res.body = pysodium.crypto_box_open_afternm(res.body,res.nonce,shared_key)
    return res

def serialize_query(body, auth = b""):
    bee = bee_pb2.query_proto()
    bee.body = body
    bee.header.host = "127.0.0.1"
    bee.header.user_agent = "python"
    bee.header.content_type = "text/plain"
    bee.header.authorization = auth
    return bee.SerializeToString()

def unserialize_reply(rep,shared_key):
    r = bee_pb2.reply_proto()
    r.ParseFromString(unserialize_response_enc(rep, shared_key).body)
    return r

class Request:
    def __init__(self, action, body, token = b""):
        self.action = action
        self.body = body
        self.token = token
        self.server_public_key = b""
        self.server_diffie = {}
        self.public_key = b""
        self.secret_key = b""
        self.shared_key = b""
        
    def send(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ("localhost", 1805)
        
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ("localhost", 1805)
            
            client_socket.connect(server_address)
            print("Connected to server:", server_address)
            
            client_socket.sendall(serialize_request("get-spk", False, b"", b""))
            res_spk = unserialize_response(client_socket.recv(1024))
            self.server_public_key = res_spk.body
            
            client_socket.sendall(serialize_request("get-dpk", False, b"", b""))
            self.server_diffie = unserialize_response(client_socket.recv(1024))
            
            try:
                pysodium.crypto_sign_verify_detached(self.server_diffie.signature, self.server_diffie.body, self.server_public_key)
                self.public_key, self.secret_key = pysodium.crypto_box_keypair()
                self.shared_key = pysodium.crypto_box_beforenm(self.server_diffie.body, self.secret_key)
                
                client_socket.sendall(serialize_request("post-cpk", False, b"", self.public_key))
                res_cpk = unserialize_response(client_socket.recv(1024))
                
                nonce = pysodium.randombytes(pysodium.crypto_box_NONCEBYTES)
                ciphertext = pysodium.crypto_box_afternm(serialize_query(self.body, self.token), nonce, self.shared_key)
                
                client_socket.sendall(serialize_request(self.action, True, nonce, ciphertext))
                return unserialize_reply(client_socket.recv(1024), self.shared_key)
                
            except ValueError:
                print("error verifying public key")            
        finally:
            client_socket.close()
            
            
def pack_user():
    user = user_pb2.user_transit_proto()
    user.username = "bumbledb"
    user.password = "optimus-prime"
    return user.SerializeToString()
  
reg = Request("user-register", pack_user()).send()          
log = Request("user-login", pack_user()).send()

my_dict = {
    "name": "John Doe",
    "age": 30,
    "city": "New York"
}

obj = Compose("dict", my_dict)
print(obj)

prot = Request("cache-save", str(obj).encode("utf-8"), log.body).send()
print(prot)

prot = Request("cache-get", b"dict", log.body).send()
print(prot.body.decode("utf-8"))
print(load.load(prot.body.decode("utf-8")))