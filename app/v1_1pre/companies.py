from app import render_template, flash
from app.models import User, Tag, Company, Position, Application
from flask import session


class Companies:

	@staticmethod
	def homepage():
		return render_template('company/homepage.html', positions=Position.query.filter(Position.company_id == session['company_id']).filter(Position.available	== True).order_by(Position.id.desc()).limit(5))

	@staticmethod
	def browse_students():
		return render_template('company/browse_students.html',
							   positions=Position.query.filter(Position.company_id == int(session['company_id'])),
							   students=Application.query.filter(Application.company_id == int(session['company_id'])))

	@staticmethod
	def my_offers():
		return render_template('company/my_offers.html',
							   positions=Position.query.filter(Position.company_id == int(session['company_id'])),
							   students=Application.query.filter(Application.company_id == int(session['company_id'])))

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
		if len(Position.query.filter(Position.id == positionId).filter(Position.available == True).all()) == 0:
			flash('This position is not available.', 'danger')
			return render_template('template.html'), 404

		position = Position.query.filter(Position.id == positionId).filter(Position.available == True)[0]
		if position.company_id == session['company_id']:
			return render_template('company/position.html', position=position)
		else:
			return render_template('students/position.html', position=position)

	@staticmethod
	def profile():
		company = Company.query.filter(Company.id == session['company_id'])[0]
		return render_template('company/profile.html', company=company)

