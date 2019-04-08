from app import app, babel, db, migrate, render_template
from app.models import insert_user, User, Tag, Company, Position, crypto
from flask import request, session, flash, redirect, url_for, send_file
import sys

# Set the secret key to some random bytes. Keep this really secret!
from datetime import timedelta
app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SESSION_TYPE'] = 'filesystem' #redis
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)

app.config.from_object(__name__)

from uuid import uuid4

def random():
	session['number'] = str(uuid4())
	return None


@babel.localeselector
def get_locale():
	translations = [str(translation) for translation in babel.list_translations()]
	print(translations)
	return request.accept_languages.best_match(translations)


@app.after_request
def set_response_headers(response):
	response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '0'
	return response


@app.before_request
def init_session():
	if 'type' not in session:
		session['type'] = 'Visitor'


@app.route('/background.png')
def image():
	if session['type'] == 'Visitor':
		filename = '2page.png'
	elif session['type'] == 'Company':
		filename = '2page.png'
	else:
		filename = 'RIS.png'
	return send_file('static/img/' + filename, mimetype='image/png')


@app.route('/')
def index():
	return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
	# note that we set the 404 status explicitly
	flash(request.full_path + ': Error 404: Page not found.', 'danger')
	return render_template('template.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
	flash(request.full_path + ': Error 500: Could be caused by invalid parameters.', 'danger')
	return render_template('template.html'), 500


@app.route('/register/company', methods=['GET', 'POST'])
def company_signup():
	print(request.form, file=sys.stderr)
	if request.method == 'POST':
		logout()
		if len(Company.query.filter(Company.uid == request.form['company_code']).all()) == 1 \
			and (request.form['password'] == request.form['verify_password'])\
			and (len(User.query.filter(User.email == request.form['email']).all()) == 0):

			insert_user(request.form['fname'] + ' ' + request.form['lname'],
						request.form['email'],
						request.form['password'],
						Company.query.filter(Company.uid == request.form['company_code']).one())

			session['email'] = request.form['email']
			session['company_id'] = Company.query.filter(Company.uid == request.form['company_code']).one().id
			session['name'] = request.form['fname'] + ' ' + request.form['lname']
			session['company'] = Company.query.filter(Company.uid == request.form['company_code']).one().name
			session['type'] = 'Company'
			random()

			return redirect(url_for('v1pre_routes.create_offer'))
		else:
			flash('Company is already registered or passwords are not matching.', 'danger')
			return redirect(url_for('company_signup'))
	else:
		return render_template('company/register.html')


@app.route('/login/company', methods=['GET', 'POST'])
def company_login():
	logout()
	if request.method == 'POST':
		if len(User.query.filter(User.email == request.form['email']).all()) == 1:
			user = User.query.filter(User.email == request.form['email']).one()

			if user.password_hash != crypto(request.form['password']):
				flash('Incorrect password.', 'danger')
				return redirect(url_for('company_login'))

			session['email'] = request.form['email']
			session['company_id'] = user.company_id
			session['name'] = user.name
			session['company'] = user.company.name
			session['type'] = 'Company'
			random()

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


@app.route('/login/student', methods=['GET', 'POST'])
def student_login():
	logout()
	if request.method == 'POST':
		if len(User.query.filter(User.email == request.form['email']).all()) == 1:
			curr = User.query.filter(User.email == request.form['email']).one()
			if curr.password_hash != crypto(request.form['password']):
				flash('Incorrect password.', 'danger')
				return redirect(url_for('student_login'))

			session['email'] = request.form['email']
			session['id'] = curr.id
			if curr.company_id:
				session['company_id'] = curr.company_id
				session['type'] = 'Company'
				session['name'] = curr.name
				session['company'] = curr.company.name
			else:
				session['name'] = curr.name
				session['company_id'] = None
				session['type'] = 'Student'
			random()

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
				and (request.form['password'] == request.form['verify_password']):

			insert_user(request.form['name'], request.form['email'], request.form['password'])

			session['email'] = request.form['email']
			session['name'] = User.query.filter(User.email == request.form['email']).filter(
				User.type_registration == request.form['type']).all()[0].name
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
	session['email'] = None
	session['id'] = None
	session['company_id'] = None
	session['type'] = 'Visitor'
	session['name'] = None
	session['company'] = None

	return redirect('/p')


@app.route('/terms')
def terms():
	return render_template('terms.html')


from app.v1_1pre.v1_1pre import routes

app.register_blueprint(routes, url_prefix='/p')

from app.blog.blog import routes
app.register_blueprint(routes, url_prefix='/blog')