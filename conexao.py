import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

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


def config_jwt():

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    jwt = JWTManager(app)

    return jwt


db = init_app(app)
