import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config(object):
    with open('/run/secrets/csrf_token', 'r') as f:
        SECRET_KEY = f.read().strip()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
