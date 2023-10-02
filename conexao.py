import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import subprocess


app = Flask(__name__)

def init_app(app=None):

    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')

    if not app:
        print('passou aqui')
        return DATABASE_URL

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['DEBUG'] = True

    db = SQLAlchemy(app)

    return db

db = init_app(app)
