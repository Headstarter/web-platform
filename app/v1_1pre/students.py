from app import render_template, flash
from app.models import User, Tag, Company, Position


class Students:

	@staticmethod
	def company_view(companyId):
		company = Company.query.filter(Company.id == companyId)[0]
		return render_template('students/company.html', company=company)

	@staticmethod
	def sector_view(sectorId):
		return render_template('students/sector.html', sector=Sector.query.filter(Sector.id == sectorId)[0], companies=Company.query.filter(Company.sector_id == sectorId).all())

	@staticmethod
	def position_view(positionId):
		if len(Position.query.filter(Position.id == positionId).filter(Position.available == True).all()) == 0:
			flash('This position is not available.', 'danger')
			return render_template('template.html'), 404

		return render_template('students/position.html', position=Position.query.filter(Position.id == positionId).filter(Position.available == True)[0])

	@staticmethod
	def all_positions_view(positionId):
		return render_template('students/position.html', position=Position.query.filter(Position.id == positionId).filter(Position.available == True)[0])


