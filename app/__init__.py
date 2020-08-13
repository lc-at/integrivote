import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')

for config_key in ('STUDENTS_CSV', ):
    if not app.config[config_key].startswith(os.path.sep):
        app.config[config_key] = os.path.join(app.root_path,
                                              app.config[config_key])

db = SQLAlchemy(app)

from .admin import bp as admin_bp  # noqa: E402,F401,F403
from .api import bp as api_bp  # noqa: E402,F401,F403
from .views import *  # noqa: E402,F401,F403

app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)
