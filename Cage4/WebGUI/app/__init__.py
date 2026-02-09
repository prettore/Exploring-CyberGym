from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALMCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "JNNOAISNDAISDOIASIASIDJOIAJOISOIJDOI"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# from app.routes import *
# Sometimes it is necessary

from app.routes import homepage
from app.models import Contato