from app import app, babel, db, migrate, render_template
from app.models import insert_user, User, Sector, Company, Position
from flask import request, session, flash, redirect, url_for
from flask_session import Session

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'

# Check Configuration section for more details
import os
from datetime import timedelta
SECRET_KEY = os.urandom(24)
SESSION_TYPE = 'filesystem' #redis
SESSION_PERMANENT = True
PERMANENT_SESSION_LIFETIME = timedelta(days=31)

app.config.from_object(__name__)
sess = Session(app)

sess.init_app(app)


@babel.localeselector
def get_locale():
	translations = [str(translation) for translation in babel.list_translations()]
	print(translations)
	return request.accept_languages.best_match(translations)


@app.before_request
def init_session():
	if 'type' not in session:
		session['type'] = 'Visitor'


@app.route ('/')
def index():
	return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
	# note that we set the 404 status explicitly
	flash(request.full_path + ': Error 404: Page not found.', 'danger')
	return render_template('template.html'), 404


@app.route('/login/company', methods=['GET', 'POST'])
def company_login():
	if request.method == 'POST':
		if len(User.query.filter(User.email == request.form['email']).filter(
				User.type_registration == request.form['type']).all()) == 1:
			session['email'] = request.form['email']
			session['company_id'] = User.query.filter(User.email == request.form['email']).filter(
				User.type_registration == request.form['type']).all()[0].company_id
			session['company'] = User.query.filter(User.email == request.form['email']).filter(
				User.type_registration == request.form['type']).all()[0].company.name
			session['type'] = 'Company'

			if 'redirect' in session:
				redirect_url = session['redirect']
				session.pop('redirect')
				return redirect(redirect_url)
			else:
				return redirect('/p')
		else:
			flash('User is not registered or user is not login by the correct way.', 'danger')
			return redirect(url_for('company_login'))
	else:
		return render_template('company/login.html')


@app.route('/signup/company', methods=['GET', 'POST'])
def company_signup():
	return render_template('company/register.html')


@app.route('/login/student', methods=['GET', 'POST'])
def student_login():
	if request.method == 'POST':
		if len(User.query.filter(User.email == request.form['email']).filter(
				User.type_registration == request.form['type']).all()) == 1 :
			session['email'] = request.form['email']
			session['name'] = User.query.filter(User.email == request.form['email']).filter(
				User.type_registration == request.form['type']).all()[0].username
			session['company_id'] = None
			session['type'] = 'Student'

			if 'redirect' in session:
				redirect_url = session['redirect']
				session.pop('redirect')
				return redirect(redirect_url)
			else:
				return redirect('/p')
		else:
			flash('User is not registered or user is not login by the correct way.', 'danger')
			return redirect(url_for('student_login'))
	else:
		return render_template('students/login.html')


@app.route('/signup/student', methods=['GET', 'POST'])
def student_signup():
	if request.method == 'POST':
		if len(User.query.filter(User.email == request.form['email']).all()) == 0 \
				and (request.form['type'] == 'fb'
				or request.form['password'] == request.form['verify_password']):

			insert_user(request.form['name'], request.form['email'], request.form['password'], request.form['type'])

			session['email'] = request.form['email']
			session['name'] = User.query.filter(User.email == request.form['email']).filter(
				User.type_registration == request.form['type']).all()[0].username
			session['company_id'] = None
			session['type'] = 'Student'

			return redirect('/p')
		else:
			flash('User is already registered or passwords does not match.', 'danger')
			return redirect(url_for('student_signup'))
	else:
		return render_template('students/register.html')


@app.route('/logout')
def logout():
	try:
		session.pop('email')
	except:
		pass

	try:
		session.pop('name')
	except:
		pass

	try:
		session.pop('company_id')
	except:
		pass

	try:
		session.pop('type')
	except:
		pass

	session['type'] = 'Visitor'

	return redirect('/p')


from app.v1pre.v1pre import routes

app.register_blueprint(routes, url_prefix='/p')

from app.blog.blog import routes
app.register_blueprint(routes, url_prefix='/blog')