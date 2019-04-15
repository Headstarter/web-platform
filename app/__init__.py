from flask import Flask, render_template, flash
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from app import sessions

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
babel = Babel(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

path = app.config['APP_ROOT'] + '/flask_session'
if not os.path.exists(path):
    os.mkdir(path)
    os.chmod(path, int('700', 8))
app.session_interface = sessions.PickleSessionInterface(path)

from app import models

from app import router