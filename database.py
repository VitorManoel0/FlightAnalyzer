from app import db


class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(150))
    password = db.Column(db.String(150))

    def __init__(self, user, password):
        self.user = user
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


