from flask import Flask, session, render_template, flash
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
babel = Babel(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from datetime import timedelta
app.permanent_session_lifetime = timedelta(days=30)

from app import models

from app import router