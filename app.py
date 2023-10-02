from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dados
from conexao import init_app

app = Flask(__name__)

db = init_app(app)

@app.route('/')
def hello_world():  # put application's code here
    db.create_all()
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
