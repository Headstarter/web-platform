from app.decorators import *
from app import app, babel, db, migrate, render_template
from app.models import User, Sector, Company, Position
from flask import g, request
from app.v1pre.v1pre import Blueprint
from app.v1pre.config import *

routes = Blueprint('visitor_routes', __name__, template_folder=template_f, static_folder=static_f)


@routes.route('/')
@require(role=None)
def homepage():
    return render_template('visitor/homepage.html',
                           positions=Position.query.order_by(Position.id.desc()).limit(5),
                           companies=len(Company.query.all()),
                           internships=len(Position.query.all()))
