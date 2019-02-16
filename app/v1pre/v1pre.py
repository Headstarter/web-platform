from app import app, babel, db, migrate, render_template
from app.models import User, Sector, Company, Position
from flask import g, request, Blueprint

from app.v1pre.visitors import routes as visitors_routes
from app.v1pre.students import routes as students_routes
from app.v1pre.companies import routes as companies_routes
