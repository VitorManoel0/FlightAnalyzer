from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField, SelectField
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib.pyplot as plt

from database import search_options_mercado, search_options_mes, search_options_ano, Flights


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
    ano_inicio = SelectField('Selecione o ano inicial do intervalo')
    ano_final = SelectField('Selecione o ano final do intervalo')
    mes_inicio = SelectField('Selecione o mês de inicio do intervalo')
    mes_final = SelectField('Selecione o mês de inicio do intervalo')
    filtrar = SubmitField('Filtrar')


def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256')


def verify_password(hashed_password, password):
    return check_password_hash(hashed_password, password)


def fill_form_filter():
    # configurar o primeiro parametro
    form = FormFilter()

    options_mercado = search_options_mercado()
    form.mercado.choices = options_mercado

    options_mes = search_options_mes()
    form.mes_inicio.choices = options_mes
    form.mes_final.choices = options_mes

    options_ano = search_options_ano()
    form.ano_inicio.choices = options_ano
    form.ano_final.choices = options_ano

    return form


def gera_grafico(mercado, ano_i=0, ano_f=0, mes_i=0, mes_f=0):
    dados = Flights.query.filter(Flights.mercado == mercado,
                                 Flights.ano >= ano_i,
                                 Flights.ano <= ano_f,
                                 Flights.mes >= mes_i,
                                 Flights.mes <= mes_f).all()

    # Crie o gráfico usando Matplotlib
    x = [d.ano for d in dados]
    y = [d.rpk for d in dados]
    plt.plot(x, y)
    plt.xlabel('Ano')
    plt.ylabel('RPK')
    plt.title('Gráfico de RPK')
    plt.grid(True)

    # Salve o gráfico em um arquivo ou exiba na página
    plt.savefig('static/grafico.png')
