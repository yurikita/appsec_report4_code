from flask import Flask, render_template, redirect, request, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm, RegistrationForm, SpellCheckForm, AdminHistoryForm
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
import subprocess
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.init_app(app)

from models import User, QueryHistory, LoginHistory
db.create_all()

#Initialize admin account
admin = User.query.filter_by(uname = 'admin').first()
if admin is None:
    admin = User(uname = 'admin', mfa = '12345678901')
    with open('/run/secrets/admin_pass', 'r') as f:
        admin.set_password(f.read().strip())
    db.session.add(admin)
    db.session.commit()

@app.route('/')
@app.route('/index')
def index():
    return redirect('/login')

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
            log = LoginHistory(uname=user.uname)
            db.session.add(log)
            db.session.commit()

    return render_template('login.html', title='Sign In', form=form, result=result)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    log = LoginHistory.query.filter_by(uname = current_user.uname, logout = "N/A").first()
    logout_user()
    log.logout = str(datetime.now())
    db.session.add(log)
    db.session.commit()

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

            query = QueryHistory(uname=current_user.uname, inputtext=textout, misspelled=misspelled)
            db.session.add(query)
            db.session.commit()

    return render_template("spell_check.html", title="Spell Check", form=form, textout=textout, misspelled=misspelled)

@app.route('/history', methods = ['POST', 'GET'])
@login_required
def history():
    form = AdminHistoryForm()
    if form.validate_on_submit() and current_user.uname == 'admin':
        queries = QueryHistory.query.filter_by(uname = form.userquery.data)
        numqueries = queries.count()
        user = form.userquery.data
    else:
        queries = QueryHistory.query.filter_by(uname = current_user.uname)
        numqueries = queries.count()
        user = current_user.uname
    return render_template("history.html", title="History", form=form, user = user, numqueries=numqueries, queries=queries)

@app.route('/history/query<id>')
@login_required
def query(id):
    query = QueryHistory.query.filter_by(id=id).first()
    return render_template("query.html", query=query)

@app.route('/login_history', methods=['POST', 'GET'])
@login_required
def login_history():
    form = AdminHistoryForm()
    user = ''
    loginqueries = []
    if form.validate_on_submit() and current_user.uname == 'admin':
        user = form.userquery.data
        loginqueries = LoginHistory.query.filter_by(uname=form.userquery.data)
    return render_template("login_history.html", form=form, user=user,loginqueries=loginqueries)

if __name__ == '__main__':
    app.run(debug=True)

