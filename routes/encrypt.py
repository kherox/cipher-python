from cryptography.fernet import Fernet
from flask_restful import Resource, Api
from flask import Flask , request 
import struct



from core.key_backend import KeyBackend


backend = KeyBackend()


class EncryptData(Resource):
    def post(self):
        data = request.get_json()
        if data is not None :
            return self.cipher(data)

    def cipher(self,values):
        cipher_suite = backend.fernet
        cipher_value = []
        content = "" 
        for val in values:
            if (isinstance(values[val] , int)):
                value = bytes(struct.pack("i" , values[val]))
                cipher_value.append({val : cipher_suite.encrypt(value)})
            elif (isinstance(values[val] , float)):
                value = bytes(struct.pack("f" , values[val]))
                cipher_value.append({val : cipher_suite.encrypt(value)})
            else :
                cipher_value.append({val :cipher_suite.encrypt(values[val].encode('utf8')) })
                content += values[val].encode('utf8')
        backend.sha256.update(content)
        hash = backend.sha256.hexdigest()
        cipher_value.append({"hash" : hash})
        backend.storeHash(hash=hash , key=backend.key)
        return cipher_value



