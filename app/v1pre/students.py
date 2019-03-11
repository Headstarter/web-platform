from app import render_template
from app.models import User, Sector, Company, Position


class Students:

	@staticmethod
	def homepage():
		return render_template('visitor/homepage.html', positions=Position.query.order_by(Position.id.desc()).limit(5))

	@staticmethod
	def company_view(companyId):
		company = Company.query.filter(Company.id == companyId)[0]
		return render_template('students/company.html', company=company)

	@staticmethod
	def sector_view(sectorId):
		return render_template('students/sector.html', sector=Sector.query.filter(Sector.id == sectorId)[0], companies=Company.query.filter(Company.sector_id == sectorId).all())

	@staticmethod
	def position_view(positionId):
		return render_template('students/position.html', position=Position.query.filter(Position.id == positionId)[0])

	@staticmethod
	def all_positions_view(positionId):
		return render_template('students/position.html', position=Position.query.filter(Position.id == positionId)[0])


