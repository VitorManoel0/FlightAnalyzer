from conexao import db


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    username = db.Column('username', db.String(150))
    password = db.Column(db.String(150))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Flights(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    ano = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    mercado = db.Column(db.String(8), nullable=False)
    rpk = db.Column(db.Float, nullable=False)

    def __init__(self, ano, mes, mercado, rpk):
        self.ano = ano
        self.mes = mes
        self.mercado = mercado
        self.rpk = rpk


def search_user_by_name(username):
    users = User.query.filter_by(username=username).all()
    return users


def have_data():
    contador = Flights.query.count()
    if contador <= 0:
        return False
    return True


def add_user(username, password):
    try:
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        return True
    except:
        return False
