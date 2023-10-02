from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField

class FormUserLogin(FlaskForm):
    user = StringField('Nome de usuário', [validators.DataRequired(), validators.Length(min=1, max=50)])
    password = PasswordField('Senha de usuário', [validators.DataRequired(), validators.Length(min=1, max=50)])
    login = SubmitField('Login')

#
# class FormUserRegister(FlaskForm):
#     user = StringField('Nome de usuário', [validators.DataRequired(), validators.Length(min=1, max=50)])
#     user = StringField('', [validators.DataRequired(), validators.Length(min=1, max=50)])
#     login = SubmitField('Login')