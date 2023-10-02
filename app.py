from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')


app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

db = SQLAlchemy(app)


@app.route('/')
def hello_world():  # put application's code here
    db.create_all()
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
