from app import render_template
from app.models import User, Sector, Company, Position


class Visitors:

    @staticmethod
    def homepage():
        return render_template('visitor/homepage.html',
                               positions=Position.query.filter(Position.available == True).order_by(
                                   Position.id.desc()).limit(5))

    @staticmethod
    def all_positions():



        return render_template('visitor/positions.html',
                               positions=Position.query.filter(Position.available == True).order_by(
                                   Position.id.desc()).limit(5))
