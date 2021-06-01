from markupsafe import escape
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

# from flaskblog import User            

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e5e35fa0bf4eb12ad59f673c0b11ab05'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)
db.create_all()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from flaskblog import routes
