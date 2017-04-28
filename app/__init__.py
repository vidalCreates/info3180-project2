from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT

app = Flask(__name__)
app.config['SECRET_KEY'] = "this is a random key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://fshmbfalghrtee:d23e3708771485cf521f437dc2d9aa4380bc6ed02ddb17e4f19e2e4ca676c05c@ec2-54-227-237-223.compute-1.amazonaws.com:5432/d4hkdh467pa9aa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

# UPLOAD FOLDER
UPLOAD_FOLDER = "./app/static/uploads"

db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config.from_object(__name__)
from app import views
