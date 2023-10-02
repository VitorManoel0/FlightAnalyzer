from flask import Flask, render_template, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import dados
from conexao import init_app
from helpers import FormUserLogin
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

db = init_app(app)

csrf = CSRFProtect(app)


@app.route('/')
def index():
    db.create_all()
    return "Teste"

@app.route('/login')
def login():
#     request.args.get('variavel')
    form = FormUserLogin()
    return render_template('login.html', form=form)

@app.route('/autenticar' , methods=['POST'])
def autenticar():
    #wip adicionar verificador de senha
    if 'senha' == 'senha':
        session['logged_user'] = 'nome_usuario'
        flash('Usuário logado com sucesso ' +  session['logged_user'])
        return redirect('/')
    else:
        flash('Usuário não logado')
        #redirecionar para o login
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
