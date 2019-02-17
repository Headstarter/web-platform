from app import app, babel, db, migrate, render_template
from app.models import User, Sector, Company, Position
from flask import g, request, session
from flask_session import Session

# Check Configuration section for more details
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

@babel.localeselector
def get_locale():
	translations = [str(translation) for translation in babel.list_translations()]
	print (translations)
	return request.accept_languages.best_match(translations)

@app.route ('/')
def index ():
	return render_template ('index.html')

@app.route ('/login')
def login ():
	return render_template ('login.html')

@app.route ('/login/student')
def student_login ():
	return render_template ('index.html')

@app.route ('/login/company')
def company_login ():
	return render_template ('index.html')

from app.v1pre.v1pre import visitors_routes, students_routes, companies_routes

for component in [visitors_routes, students_routes, companies_routes]:
	app.register_blueprint(component, url_prefix='/v1.pre')

