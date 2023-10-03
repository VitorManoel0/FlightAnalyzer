from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField, SelectField
from werkzeug.security import generate_password_hash, check_password_hash


class FormUserLogin(FlaskForm):
    username = StringField('Nome de usuário', [validators.DataRequired(), validators.Length(min=1, max=50)])
    password = PasswordField('Senha de usuário', [validators.DataRequired(), validators.Length(min=1, max=50)])
    login = SubmitField('Login')


class FormUserRegister(FlaskForm):
    username = StringField('Nome de usuário', [validators.DataRequired(), validators.Length(min=1, max=150)])
    password = PasswordField('Senha de usuário', [validators.DataRequired(), validators.Length(min=1, max=50)])
    cadastro = SubmitField('Cadastrar')


class FormFilter(FlaskForm):
    mercado = SelectField('Selecione o mercado')
    ano = StringField('Selecione o ano')
    mes = StringField('Selecione o mês')
    filtrar = SubmitField('Filtrar')


def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256')


def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)
