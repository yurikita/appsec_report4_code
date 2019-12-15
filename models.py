from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login

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
