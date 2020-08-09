from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from .views import *  # noqa: E402,F401,F403
from .admin import bp as admin_bp  # noqa: E402,F401,F403

app.register_blueprint(admin_bp)
