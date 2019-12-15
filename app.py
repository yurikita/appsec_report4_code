from flask import Flask, render_template, redirect, request, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegistrationForm, SpellCheckForm
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
import subprocess

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
db.create_all()
login = LoginManager(app)
login.init_app(app)

from models import User

@app.route('/')
@app.route('/index')
def index():
    if not current_user.is_authorized():
        return redirect('/login')
    else:
        return redirect('/spell_check')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    form = RegistrationForm()
    success = ''
    if form.validate_on_submit():
        user = User.query.filter_by(uname=form.uname.data).first()
        if user is not None:
            success = 'failure'
        else:
            u = User(uname=form.uname.data, mfa=form.mfa.data)
            u.set_password(form.pword.data)
            db.session.add(u)
            db.session.commit()
            success = 'success'
    return render_template('register.html', title='Register', form=form, success=success)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    result = ''
    if form.validate_on_submit():
        user = User.query.filter_by(uname=form.uname.data).first()
        if user is None or not user.check_password(form.pword.data):
            result = 'Incorrect'
        elif user.mfa != form.mfa.data:
            result = 'Two-factor failure'
        else:
            result = 'Success'
            login_user(user)
    return render_template('login.html', title='Sign In', form=form, result=result)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    return redirect('/login')


@app.route('/spell_check', methods=['POST', 'GET'])
@login_required
def spell_check():
    form = SpellCheckForm()
    textout = ''
    misspelled = ''
    if form.validate_on_submit():
        inputtext = form.inputtext.data
        with open("inputtext.txt", "w") as f:
            f.write(inputtext)
            f.close()
            temp = subprocess.check_output(["./a.out", "inputtext.txt", "wordlist.txt"])
            temp = temp.decode()
            misspelled = temp.replace('\n', ', ')[:-2]
            textout = inputtext
    return render_template("spell_check.html", title="Spell Check", form=form, textout=textout, misspelled=misspelled)


if __name__ == '__main__':
    app.run(debug=True)

