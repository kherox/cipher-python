from flask import Flask , request 
from flask_restful import Resource, Api


from middleware import AuthorizationMiddleware




from routes.encrypt import EncryptData
from routes.decrypt import DecryptData

app = Flask(__name__)
app.wsgi_app = AuthorizationMiddleware(app.wsgi_app)
api = Api(app)


api.add_resource(EncryptData, '/')
api.add_resource(DecryptData, '/decrypt')

if __name__ == '__main__':
    app.run(debug=True , port=8080)
