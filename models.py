from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    uname = db.Column(db.String(64), index=True, unique=True)
    pword_hash = db.Column(db.String(128))
    mfa = db.Column(db.String(64))

    def __repr__(self):
        return '<User {}>'.format(self.uname)

    def set_password(self, password):
        self.pword_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.pword_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class QueryHistory(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    uname = db.Column(db.String(64), db.ForeignKey('user.uname'), index = True)
    inputtext = db.Column(db.String(64000))
    misspelled = db.Column(db.String(64000))
    timestamp = db.Column(db.String(64), default = str(datetime.now()))

    def __repr__(self):
        return '<User {}, queryid {}>'.format(self.uname, self.id)

class LoginHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(64), db.ForeignKey('user.uname'), index = True)
    login = db.Column(db.String(64), default = str(datetime.now()))
    logout = db.Column(db.String(64), default = "N/A")

    def __repr__(self):
        return '<User {}, login {}, logout {}>'.format(self.uname, self.login, self.logout)

