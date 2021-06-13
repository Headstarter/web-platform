from flask import Flask, session, render_template, flash
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

if 'CONFIG' in os.environ:
    os.environ['CONFIG'] = os.environ['CONFIG'] or 'config.cfg'
else:
    os.environ['CONFIG'] = 'config.cfg'

if 'FLASK_DEBUG' in os.environ:
    os.environ['FLASK_DEBUG'] = os.environ['FLASK_DEBUG'] or '1'
else:
    os.environ['FLASK_DEBUG'] = '1'

app = Flask(__name__)
app.config.from_pyfile(os.environ['CONFIG'])
babel = Babel(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from datetime import timedelta
app.permanent_session_lifetime = timedelta(days=30)

from app import models

from app import router