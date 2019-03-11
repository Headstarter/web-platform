from app import app, babel, db, migrate, render_template
from flask import session
from app.models import User, Sector, Company, Position
from flask import g, request, Blueprint, flash, url_for
from app.v1pre.config import *

from app.v1pre.visitors import Visitors
from app.v1pre.students import Students
from app.v1pre.companies import Companies

mapped_routes = {
    'Visitor': Visitors,
    'Student': Students,
    'Company': Companies
}

routes = Blueprint('v1pre_routes', __name__, template_folder=template_f, static_folder=static_f)


@routes.route('/')
def homepage():
    return mapped_routes[session['type']].homepage() or mapped_routes['Visitor'].homepage()


@routes.route('/company/<companyId>', methods=['GET', 'POST'])
def company_view(companyId):
    return mapped_routes[session['type']].company_view(companyId) or mapped_routes['Visitor'].company_view(companyId)


@routes.route('/sector/<sectorId>', methods=['GET', 'POST'])
def sector_view(sectorId):
    return mapped_routes[session['type']].sector_view(sectorId) or mapped_routes['Visitor'].sector_view(sectorId)


@routes.route('/position/<positionId>', methods=['GET', 'POST'])
def position_view(positionId):
    try:
        return mapped_routes[session['type']].position_view(positionId) or mapped_routes['Visitor'].position_view(positionId)
    except:
        flash('В момента нямате достъп до тази страница. Моля, опитайте да влезете в системата.', 'warning')
        flash('<a class="nav-link" href="#" data-toggle="modal" data-target="#student_company">Вход</a>', 'info')
        session['redirect'] = url_for('v1pre_routes.position_view', positionId=positionId)
        return render_template('template.html')

@routes.route('/update', methods=['POST'])
def update_data():
    import json
    return json.dumps(request.form['value'])
