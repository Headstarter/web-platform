from app import render_template
from app.models import User, Sector, Company, Position


class Visitors:

    @staticmethod
    def homepage():
        return render_template('visitor/homepage.html',
                               positions=Position.query.order_by(Position.id.desc()).limit(5))
