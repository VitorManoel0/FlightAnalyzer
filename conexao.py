import os
from flask_sqlalchemy import SQLAlchemy


def init_app(app=None):

    DATABASE_URL = os.getenv('DATABASE_URL')
    SECRET_KEY = os.getenv('SECRET_KEY')

    if not app:
        return DATABASE_URL

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['DEBUG'] = True

    db = SQLAlchemy(app)

    return db
