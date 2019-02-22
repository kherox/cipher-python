from flask import Flask , request 
from flask_restful import Resource, Api
from cryptography.fernet import Fernet


from core.key_backend import KeyBackend


backend = KeyBackend()



class DecryptData(Resource):

    def post(self):
        data = request.get_json()
        if data is not None :
            return self.decrypt(data)
    
    def decrypt(self,values):
        hash = values["hash"]
        hd = backend.receiveHashKey(hash=hash)
        if hd is None :
            return {"message"  : "Donnees compromis"}
        key = hd.hash_key
        backend.keys(key.encode("utf8"))
        cipher_value = []
        for val in values:
            print(val)
            if val != "hash":
                #print(values[val])
                cipher_value.append({val :backend.fernet.decrypt(values[val].encode('utf8')) })
        return cipher_value

