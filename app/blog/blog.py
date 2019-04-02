from app.decorators import *
from app import app, babel, db, migrate, render_template
from app.models import User, Tag, Company, Position
from flask import g, request
from flask import Blueprint
from app.blog.config import *

routes = Blueprint('blog_routes', __name__, template_folder=template_f, static_folder=static_f)

@routes.route ('/')
@require(role='Student')
def homepage():
    return render_template('blog/homepage.html')


