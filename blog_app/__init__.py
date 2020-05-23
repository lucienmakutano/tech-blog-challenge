try:
    from flask import Flask, url_for
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager
    from secrets import token_hex
    from flask_bcrypt import Bcrypt
except ModuleNotFoundError:
    print('module not found')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = token_hex(32)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Your session has expired.'
login_manager.login_message_category = 'warning'

bcrypt = Bcrypt(app)

from blog_app.session_manager import login, register
from blog_app.user import home
