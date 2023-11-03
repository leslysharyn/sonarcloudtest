from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from dotenv import load_dotenv
from os import getenv
from modelos import db
from vistas import Health, Ping, CreateProyect

def set_env():
    load_dotenv()
    global DATABASE_URL
    DATABASE_URL = getenv("DATABASE_URL")
    global JWT_SECRET_KEY
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
    
set_env()

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
application.config['PROPAGATE_EXCEPTIONS'] = True

app_context = application.app_context()
app_context.push()

db.init_app(application)
db.create_all()


allowed_origins = [
    "http://abcbucketfront.s3-website.us-east-2.amazonaws.com",
    "https://7vo2h4lbmd.execute-api.us-east-2.amazonaws.com",
    "http://localhost:4200"
]

cors = CORS(application, resources={r"/*": {"origins": allowed_origins, "supports_credentials": True, "allow_headers": ["Content-Type", "Authorization"]}})

api = Api(application)
api.add_resource(Health, '/')
api.add_resource(Ping, '/proyect/ping')
api.add_resource(CreateProyect, '/project')

jwt = JWTManager(application)

if __name__ == '__main__':
    application.run(port = 5000, debug = True)


