from app import render_template
from app.models import User, Sector, Company, Position
from flask import session

class Companies:

	@staticmethod
	def homepage():
		return render_template('visitor/homepage.html', positions=Position.query.filter(Position.company_id==session['company_id']).order_by(Position.id.desc()).limit(5))

	@staticmethod
	def company_view(companyId):
		company = Company.query.filter(Company.id == companyId)[0]
		if companyId == session['company_id']:
			return render_template('company/company.html', company=company)
		else:
			return render_template('students/company.html', company=company)

	@staticmethod
	def sector_view(sectorId):
		return render_template('students/sector.html', sector=Sector.query.filter(Sector.id == sectorId)[0], companies=Company.query.filter(Company.sector_id == sectorId).all())

	@staticmethod
	def position_view(positionId):
		position = Position.query.filter(Position.id == positionId)[0]
		if True: #position.company_id == session['company_id']:
			return render_template('company/position.html', position=position, a=position.company_id, b = session['company_id'])
		else:
			return render_template('students/position.html', position=position, a=position.company_id, b = session['company_id'])
