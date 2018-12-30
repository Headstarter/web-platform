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
    print ('index')
    return render_template ('index.html', companies=Company.query.all(), sectors=Sector.query.all())

@app.route ('/company/<companyId>', methods = ['GET', 'POST'])
def company_view (companyId):
	company = Company.query.filter (Company.id == companyId)[0]
	return render_template ('company.html', company=company)

@app.route ('/sector/<sectorId>', methods = ['GET', 'POST'])
def sector_view (sectorId):
    return render_template ('sector.html', sector=Sector.query.filter (Sector.id == sectorId)[0], companies=Company.query.filter(Company.sector_id == sectorId).all())
