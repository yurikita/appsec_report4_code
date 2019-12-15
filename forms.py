from flask_wtf import FlaskForm
from wtforms import PasswordField, validators, IntegerField, StringField, SubmitField, TextAreaField

class RegistrationForm(FlaskForm):
    uname = StringField('Username', [validators.DataRequired()])
    pword = PasswordField('Password', [validators.DataRequired()])
    mfa = PasswordField('2fa', id="2fa")
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    uname = StringField('Username', [validators.DataRequired()])
    pword = PasswordField('Password', [validators.DataRequired()])
    mfa = PasswordField('2fa', id="2fa")
    submit = SubmitField('Sign In')

class SpellCheckForm(FlaskForm):
    inputtext = TextAreaField('Input Text')
    submit = SubmitField('Submit')
