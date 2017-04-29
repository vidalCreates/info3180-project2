from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT

app = Flask(__name__)
app.config['SECRET_KEY'] = "this is a random key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://joxkojdnhhkixw:a95d095deb5b242f0088b39220c0937afa065aa77e8279c0bd3ad2beed481003@ec2-50-19-95-47.compute-1.amazonaws.com:5432/d1ebjlcv1ajonp'
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
