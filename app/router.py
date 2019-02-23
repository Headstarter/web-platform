from app import app, babel, db, migrate, render_template
from app.models import User, Sector, Company, Position
from flask import g, request, session, flash
from flask_session import Session
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'

# Check Configuration section for more details
SESSION_TYPE = 'raddit'
app.config.from_object(__name__)
sess = Session(app)

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

@app.route ('/login/company', methods=['GET', 'POST'])
def company_login ():
	if request.method == 'POST':
		if len(User.query.filter (User.email==request.form ['email']).filter (User.type_registration==request.form ['type']).all ()) == 1:
			session['email'] = request.form['email']
			session['company_id'] = User.query.filter (User.email==request.form ['email']).filter (User.type_registration==request.form ['type']).all()[0].company_id
			session['type'] = 'HR'

			return redirect(url_for('index'))
		else:
			flash ('User is not registered or user is not login by the correct way.')
			return redirect(url_for(company_login))
	else:
		return render_template ('company/login.html')

@app.route ('/signup/company', methods=['GET', 'POST'])
def company_signup ():
	return render_template ('company/register.html')

from app.v1pre.v1pre import visitors_routes, students_routes, companies_routes

for component in [visitors_routes, students_routes, companies_routes]:
	app.register_blueprint(component, url_prefix='/v1.pre')

