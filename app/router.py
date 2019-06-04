from app import app, babel, db, migrate, render_template
from app.models import insert_user, User, Tag, Company, Position, crypto, Mapper, insert_company
from flask import request, session, flash, redirect, url_for, send_file, Response
import sys

app.config['STATIC_FOLDER'] = '/static/wt_prod-20039'
app.secret_key = 'b94079a3717eda429c4580496be97bc9675d3ea4eb0ae50d'


def my_redirect(path):
	import flask
	response = flask.Response(response=render_template("redirect.html"), status=200)
	response.headers['X-Response-URL'] = path
	return response


@babel.localeselector
def get_locale():
	translations = ['bg', 'en']
	return request.accept_languages.best_match(translations) or 'en'


@app.after_request
def set_response_headers(response):
	response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '0'
	return response


@app.before_request
def init_session():
	if 'language' not in session or session['language'] is None:
		session['language'] = get_locale()
	# session['language'] = 'en'
	# session['language'] = get_locale()
	if '_flashes' not in session:
		session['_flashes'] = []
	if 'type' not in session:
		session['type'] = 'Visitor'
	
	print(request.full_path + ': ' + str(session) + ': ' + str(session), file=sys.stderr)


@app.route('/css/<path:filename>')
def css(filename):
	return send_file('static/wt_prod-20039/css/' + filename, mimetype='text/css')


@app.route('/js/<path:filename>')
def js(filename):
	return send_file('static/wt_prod-20039/js/' + filename, mimetype='text/javascript')


@app.route('/images/<path:filename>')
def images(filename):
	if filename.endswith('.jpg'):
		return send_file('static/wt_prod-20039/images/' + filename, mimetype='image/jpeg')
	else:
		return send_file('static/wt_prod-20039/images/' + filename, mimetype='image/png')


@app.route('/fonts/<path:filename>')
def fonts(filename):
	if filename.endswith('.svg'):
		return send_file('static/wt_prod-20039/fonts/' + filename, mimetype='image/svg+xml')
	elif filename.endswith('.eot'):
		return send_file('static/wt_prod-20039/fonts/' + filename, mimetype='application/vnd.ms-fontobject')
	elif filename.endswith('.ttf'):
		return send_file('static/wt_prod-20039/fonts/' + filename, mimetype='font/ttf')
	elif filename.endswith('.woff'):
		return send_file('static/wt_prod-20039/fonts/' + filename, mimetype='font/woff')
	elif filename.endswith('.woff2'):
		return send_file('static/wt_prod-20039/fonts/' + filename, mimetype='font/woff2')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(503)
def internal_server_error(e):
    return render_template('503.html'), 503


@app.route('/join', methods=['GET', 'POST'])
def login_register():
	type_user = 'Both'
	action = 'register'
	try:
		type_user = request.args['type']
	except KeyError:
		pass
	try:
		action = request.args['action']
	except KeyError:
		pass
	return render_template('core/' + str(session['language'] or get_locale()) + '/visitor/login-register.html', action=action, type=type_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
	
	print(request.form, file=sys.stderr)
	
	company = request.form['company']

	if company == '':
		if len(User.query.filter(User.email == request.form['email']).all()) == 0 \
                and (request.form['password'] == request.form['password-confirm']):

			insert_user(request.form['name'], request.form['email'], request.form['password'])

			session['email'] = request.form['email']
			session['name'] = User.query.filter(User.email == request.form['email']).all()[0].name
			session['id'] = User.query.filter(User.email == request.form['email']).all()[0].id
			session['company_id'] = None
			session['type'] = 'Student'

			try:
				if session['redirect']:
					return my_redirect(session['redirect'])
				else:
					return my_redirect('/')
			except:
				return my_redirect('/')
		else:
			flash('User is already registered or passwords does not match.', 'danger')
			flash('Please, just log in.', 'info')
			return my_redirect(url_for('login_register', type="Student", action='register'))
	else:
		if (request.form['password'] == request.form['password-confirm'])\
                and (len(User.query.filter(User.email == request.form['email']).all()) == 0):

			my_company = {}
			
			if Mapper.query.filter(Mapper.company_name == request.form['company']).count() == 1:
				print('\t\t\tMapper found', file=sys.stderr)
				my_company = Company.query.filter(Company.id == Mapper.query.filter(Mapper.company_name == request.form['company']).one().company_id).one()
			else:
				print('\t\t\tMapper NOT found', file=sys.stderr)
				my_company = insert_company(request.form['company'])
			print('', my_company.name, my_company.id, my_company.uid, file=sys.stderr)
			insert_user(request.form['name'], request.form['email'], request.form['password'], my_company)

			session['email'] = request.form['email']
			session['company_id'] = my_company.id
			session['name'] = request.form['name']
			session['company'] = my_company.name
			session['type'] = 'Company'
			
			try:
				if session['redirect']:
					return my_redirect(session['redirect'])
				else:
					return my_redirect('/')
			except:
				return my_redirect('/')
		else:
			flash('User is already registered or passwords are not matching.', 'danger')
			flash('Please, just log in.', 'info')
			return my_redirect(url_for('login_register', type="Company", action='register'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	
	if len(User.query.filter(User.email == request.form['email']).all()) == 1:
		user = User.query.filter(User.email == request.form['email']).one()

		if user.password_hash != crypto(request.form['password']):
			flash('Incorrect password.', 'danger')
			return redirect(url_for('login_register', action="login"))

		if user.company_id is None:
			session['email'] = request.form['email']
			session['name'] = User.query.filter(User.email == request.form['email']).all()[0].name
			session['id'] = User.query.filter(User.email == request.form['email']).all()[0].id
			session['company_id'] = None
			session['type'] = 'Student'
		else:
			session['email'] = request.form['email']
			session['company_id'] = user.company_id
			session['name'] = user.name
			session['company'] = user.company.name
			session['type'] = 'Company'

		try:
			if session['redirect']:
				return my_redirect(session['redirect'])
			else:
				return my_redirect('/')
		except:
			return my_redirect('/')
	else:
		flash('User is not registered.', 'danger')
		return my_redirect(url_for('login_register', action="login"))

"""
@app.route('/register/company', methods=['GET', 'POST'])
def company_signup():
	print(request.form, file=sys.stderr)
	if request.method == 'POST':
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

			return redirect(url_for('v1pre_routes.create_offer'))
		else:
			flash('Company is already registered or passwords are not matching.', 'danger')
			return redirect(url_for('company_signup'))
	else:
		return render_template('company/register.html')


@app.route('/login/company', methods=['GET', 'POST'])
def company_login():
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

			return redirect('/p')
		else:
			flash('User is not registered or user is not login by the correct way.', 'danger')
			return redirect(url_for('company_login'))
	else:
		return render_template('company/login.html')


@app.route('/login/student', methods=['GET', 'POST'])
def student_login():
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
			try:
				if session['redirect']:
					return redirect(session['redirect'])
				else:
					return redirect('/p')
			except:
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
			session['name'] = User.query.filter(User.email == request.form['email']).all()[0].name
			session['id'] = User.query.filter(User.email == request.form['email']).all()[0].id
			session['company_id'] = None
			session['type'] = 'Student'

			try:
				if session['redirect']:
					return redirect(session['redirect'])
				else:
					return redirect('/p')
			except:
					return redirect('/p')
		else:
			flash('User is already registered or passwords does not match.', 'danger')
			return redirect(url_for('student_signup'))
	else:
		return render_template('students/register.html')
"""

@app.route('/logout')
def logout():
	session['email'] = None
	session['id'] = None
	session['company_id'] = None
	session['type'] = 'Visitor'
	session['name'] = None
	session['company'] = None
	session['redirect'] = None
	session['language'] = get_locale()

	return redirect('/p')


@app.route('/terms')
def terms():
	return render_template('privacy-policy.html')


from app.v1.core import routes

app.register_blueprint(routes, url_prefix='/')

from app.blog.blog import routes
app.register_blueprint(routes, url_prefix='/blog')