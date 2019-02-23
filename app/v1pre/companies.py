from app.decorators import *
from app import app, babel, db, migrate, render_template
from app.models import User, Sector, Company, Position
from flask import g, request
from app.v1pre.v1pre import Blueprint
from app.v1pre.config import *

routes = Blueprint('company_routes', __name__, template_folder=template_f, static_folder=static_f)

@routes.route ('/')
@require(role='Company')
def homepage ():
    return render_template ('homepage.html', companies=Company.query.all(), sectors=Sector.query.all())

@routes.route ('/company/<companyId>', methods = ['GET', 'POST'])
@require(role='Company')
def company_view (companyId):
	company = Company.query.filter (Company.id == companyId)[0]
	return render_template ('company/company.html', company=company)

@routes.route ('/sector/<sectorId>', methods = ['GET', 'POST'])
@require(role='Company')
def sector_view (sectorId):
    return render_template ('company/sector.html', sector=Sector.query.filter (Sector.id == sectorId)[0], companies=Company.query.filter(Company.sector_id == sectorId).all())

@routes.route ('/position/<positionId>', methods = ['GET', 'POST'])
@require(role='Company')
def position_view (positionId):
	return render_template ('company/position.html', position=Position.query.filter (Position.id == positionId)[0])


