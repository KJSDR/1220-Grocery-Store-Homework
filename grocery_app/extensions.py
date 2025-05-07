from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from grocery_app.config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Initialize Flask-Bcrypt
bcrypt = Bcrypt(app)

# Import User model for user loader function
# (import here to avoid circular imports)
from grocery_app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))