from app import app, babel, db, migrate, render_template
from app.models import User, Sector, Company
from flask import g, request

@babel.localeselector
def get_locale():
	translations = [str(translation) for translation in babel.list_translations()]
	print (translations)
	return request.accept_languages.best_match(translations)

@app.route ('/')
def index ():
   return render_template ('index.html', sectors=Sector.query.all())

@app.route ('/company/<companyId>', methods = ['GET', 'POST'])
def company_view (companyId):
	return ''

@app.route ('/sector/<sectorId>', methods = ['GET', 'POST'])
def sector_view (sectorId):
   return render_template ('sector.html', companies=Company.query.filter(Company.sector_id == sectorId))
