from app import app, babel, db, migrate, render_template
from app.router import session
from app.models import User, Tag, Company, Position
from flask import g, request, Blueprint, flash, url_for
from app.v1.config import *

routes = Blueprint('blog_routes', __name__, template_folder=template_f, static_folder=static_f)

@routes.route('/')
def homepage():
    return ''