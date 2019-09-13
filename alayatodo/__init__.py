from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# configuration
DATABASE = '/tmp/alayatodo.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)

import alayatodo.views
