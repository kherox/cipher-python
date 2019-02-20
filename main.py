
from cryptography.fernet import Fernet
import redis

from flask import Flask , request 
from flask_restful import Resource, Api


from middleware import AuthorizationMiddleware

app = Flask(__name__)
app.wsgi_app = AuthorizationMiddleware(app.wsgi_app)
api = Api(app)

"Cipher config"

key = Fernet.generate_key()
r = redis.Redis()

r.set("key",key)

all_hosts = ["127.0.0.1"]

def cipher(value):
    cipher_suite = Fernet(r.get('key'))
    cipher_text = cipher_suite.encrypt(value.encode('utf8'))
    return cipher_text

def decrypt(cipher_text):
    cipher_suite = Fernet(r.get('key'))
    plain_text = cipher_suite.decrypt(cipher_text.encode("utf-8"))
    return plain_text

class EncryptData(Resource):
    def post(self):
        data = request.get_json()
        if data.get('value') is not None :
            return {"cipher" : cipher(data.get('value'))}


class DecryptData(Resource):
    def post(self):
        data = request.get_json()
        if data.get('cipher') is not None :
            return {"value" : decrypt(data.get('cipher'))}

api.add_resource(EncryptData, '/')
api.add_resource(DecryptData, '/decrypt')

if __name__ == '__main__':
    app.run(debug=True)
