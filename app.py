from flask import render_template, session, flash, redirect, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, verify_jwt_in_request
from conexao import app, db, config_jwt
from database import search_user_by_name, add_user, have_data, search_options_mercado, search_options_mes, \
    search_options_ano
from helpers import FormUserLogin, FormUserRegister, hash_password, verify_password, FormFilter, fill_form_filter, \
    gera_grafico, have_grafico
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from dados import filter_data
import ast

csrf = CSRFProtect(app)

migrate = Migrate(app, db)

jwt = config_jwt()


@app.route('/')
def index():
    # conferir ID = 2554/1558
    if not have_data():
        print('-------------loading data-------------')
        filter_data()
        print('-------------finish loading data-------------')
    return render_template('index.html')


@app.route('/login')
def login():
    #     request.args.get('variavel')
    form = FormUserLogin()
    return render_template('login.html', form=form)


@app.route('/cadastro', methods=['POST', 'GET'])
def cadastro():
    page = 'cadastro'
    form = FormUserRegister()
    return render_template('cadastro.html', form=form, page=page)


@app.route('/autenticar', methods=['POST', 'GET'])
def autenticar():
    form = FormUserLogin(request.form)

    user = search_user_by_name(form.username.data)

    if verify_password(user.password, form.password.data):
        create_access_token(identity=form.username.data)
        flash('Usuário logado com sucesso')
        return redirect('/filtro')
    else:
        flash('nickname ou senha incorreto')
        return redirect('/login')


@app.route('/autenticar_cadastro', methods=['POST', 'GET'])
def autenticar_cadastro():
    form = FormUserRegister(request.form)

    if form.validate_on_submit():
        users = search_user_by_name(form.username.data)
        if users:
            flash('Usuário ja existente')
            return redirect('/login')

        user_add = add_user(form.username.data, hash_password(form.password.data))

        if user_add:
            access_token = create_access_token(identity=form.username.data)
            if access_token:
                # Verificar JWT issues
                # verify_jwt_in_request()
                # flash('Usuário ' + get_jwt_identity() + ' logado com sucesso')
                flash('Usuário logado com sucesso')
                # Pagina de ver aviões
                return redirect('/')
        else:
            flash('Ocorreu um erro desconhecido, tente novamente')
            return redirect('/cadastro')


@app.route('/filtro')
def filtro():
    form = fill_form_filter()

    return render_template('filtro.html', form=form)


@app.route('/grafico', methods=['POST', 'GET'])
def grafico():
    # Consulte o banco de dados para obter os dados do gráfico
    form = FormFilter(request.form)

    data = gera_grafico(mercado=ast.literal_eval(form.mercado.data)[1],
                        ano_i=ast.literal_eval(form.ano_inicio.data)[0],
                        ano_f=ast.literal_eval(form.ano_final.data)[0],
                        mes_i=ast.literal_eval(form.mes_inicio.data)[0],
                        mes_f=ast.literal_eval(form.mes_final.data)[0])

    form = fill_form_filter()

    if data:
        path = have_grafico(True)
        if path:
            grafico = path
        else:
            grafico = 'none'

    else:
        grafico = 'none'

    return render_template('filtro.html', form=form, grafico=grafico)


@app.route('/logout')
def logout():
    session['logged_user'] = None
    flash('Logout efetuado com sucesso!')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
