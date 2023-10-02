from flask import Flask, render_template, session, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from conexao import init_app, app, db
from database import search_user_by_name, add_user, have_data
from helpers import FormUserLogin, FormUserRegister, hash_password
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from dados import filter_data

csrf = CSRFProtect(app)

migrate = Migrate(app, db)


@app.route('/')
def index():
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
    # wip adicionar verificador de senha
    if 'senha' == 'senha':
        session['logged_user'] = 'nome_usuario'
        flash('Usuário logado com sucesso ' + session['logged_user'])
        return redirect('/')
    else:
        flash('Usuário não logado')
        # redirecionar para o login
        return redirect('/')

    # form = FormUserLogin(request.form)
    print('funcionou')
    return 'Funcionou'


@app.route('/autenticar_cadastro', methods=['POST', 'GET'])
def autenticar_cadastro():
    form = FormUserRegister(request.form)

    if form.validate_on_submit():
        users = search_user_by_name(form.username.data)
        if users:
            flash('Usuário ja existente')
            return redirect('/login')

        add_user(form.username.data, hash_password(form.password.data))
        session['logged_user'] = 'nome_usuario'
        flash('Usuário logado com sucesso ' + session['logged_user'])
        return redirect('/')
    else:
        flash('Usuário não logado')
        # redirecionar para o login
        return redirect('/')

    form = FormUserLogin(request.form)
    print('funcionou')
    return 'Funcionou'


@app.route('/logout')
def logout():
    session['logged_user'] = None
    flash('Logout efetuado com sucesso!')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
