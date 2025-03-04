from app import app, babel, db, migrate, render_template
from app.models import Verify, insert_user, User, Tag, Company, Position, crypto, Mapper, insert_company, School
from flask import request, session, flash, redirect, url_for, send_file, Response
import sys

app.config['STATIC_FOLDER'] = '/static/headstarter'
app.secret_key = 'b94079a3717eda429c4580496be97bc9675d3ea4eb0ae50d'

def my_redirect(path, redirect_action='reload', html=''):
    import flask
    if redirect_action == 'reload':
        response = flask.Response(response=redirect(path).data, status=200)
    else:
        response = flask.Response(response=html, status=200)
    response.headers['X-Response-URL'] = path
    response.headers['X-Redirect-Same-Page'] = redirect_action
    return response


def get_locale():
    translations = ['bg', 'en']
    return request.accept_languages.best_match(translations) or 'en'

babel.init_app(app, locale_selector=get_locale)


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'public, max-age=300, must-revalidate, no-store'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.before_request
def init_session():
    if 'language' not in session or session['language'] is None:
        session['language'] = get_locale()
    session['language'] = 'bg'
    # session['language'] = get_locale()
    if '_flashes' not in session:
        session['_flashes'] = []
    if 'type' not in session:
        session['email'] = None
        session['id'] = None
        session['company_id'] = None
        session['type'] = 'Visitor'
        session['name'] = None
        session['company'] = None
        session['redirect'] = None
        

    print(request.full_path + ': ' + str(session) + ': ' + str(session))


@app.route('/css/<path:filename>')
def css(filename):
    return send_file('static/headstarter/css/' + filename, mimetype='text/css')


@app.route('/js/<path:filename>')
def js(filename):
    return send_file('static/headstarter/js/' + filename, mimetype='text/javascript')


@app.route('/images/<path:filename>')
def images(filename):
    if filename.endswith('.jpg'):
        return send_file('static/headstarter/images/' + filename, mimetype='image/jpeg')
    else:
        return send_file('static/headstarter/images/' + filename, mimetype='image/png')


@app.route('/fonts/<path:filename>')
def fonts(filename):
    if filename.endswith('.svg'):
        return send_file('static/headstarter/fonts/' + filename, mimetype='image/svg+xml')
    elif filename.endswith('.eot'):
        return send_file('static/headstarter/fonts/' + filename, mimetype='application/vnd.ms-fontobject')
    elif filename.endswith('.ttf'):
        return send_file('static/headstarter/fonts/' + filename, mimetype='font/ttf')
    elif filename.endswith('.woff'):
        return send_file('static/headstarter/fonts/' + filename, mimetype='font/woff')
    elif filename.endswith('.woff2'):
        return send_file('static/headstarter/fonts/' + filename, mimetype='font/woff2')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(503)
def internal_server_error(e):
    return render_template('503.html'), 503

import os
def get_sitekey():
    try:
        if os.environ['DEBUG'] == 'on':
            return '6LcFN3kUAAAAAEceLTlBxXFKoCXAIUpmKbKuqPHF'
        else:
            return '6LczBawUAAAAACE80VhK_L7NYXKvFaaecgBPlHXi'
    except:
        return '6LczBawUAAAAACE80VhK_L7NYXKvFaaecgBPlHXi'

def get_secretkey():
    try:
        if os.environ['DEBUG'] == 'yes':
            return '6LcFN3kUAAAAAAP1dYevtJcXYqKPWgcBL6YdWbtl'
        else:
            return '6LczBawUAAAAAIM-ca8Z8nKu-CIRnr5F1H03YOIV'
    except:
        return '6LczBawUAAAAAIM-ca8Z8nKu-CIRnr5F1H03YOIV'

@app.route('/join', methods=['GET', 'POST'])
def login_register():
    type_user = 'Undefined'
    action = 'register'
    try:
        type_user = request.args['type']
    except KeyError:
        pass
    try:
        action = request.args['action']
    except KeyError:
        pass

    print('\n\n\n\n', Company.query.all(), '\n\n\n\n\n\n')

    return render_template('core/' + str(session['language'] or get_locale()) + '/visitor/login-register.html', sitekey=get_sitekey(), action=action, type=type_user, companies=Company.query.all(), schools=School.query.all())

@app.route('/asdf')
def shit():
    return render_template('core/bg/visitor/Direktor_registration.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    print(request.form)
    
    member = request.form['member']
    
    if member == 'company':
        company = request.form['company']
    if member == 'school':
        school = request.form['school']

    if len(request.form['email']) >= 6 and len(request.form['password']) >= 8 and len(request.form['name']) >= 3:
        if member == 'student':
            import requests

            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={'secret': get_secretkey(), 'response': request.form['g-recaptcha-response'], 'remoteip': request.remote_addr})
            if len(User.query.filter(User.email == request.form['email']).all()) == 0 and (request.form['password'] == request.form['password-confirm']):
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
                if len(User.query.filter(User.email == request.form['email']).all()) != 0:
                    flash('User is already registered. Please, just log in.', 'danger')
                elif request.form['password'] != request.form['password-confirm']:
                    flash('Passwords does not match.', 'info')
                return my_redirect(url_for('login_register', type="Student", action='register'))
        elif member == 'school':
            if (request.form['password'] == request.form['password-confirm'])\
                    and (len(User.query.filter(User.email == request.form['email']).all()) == 0):
                
                if request.form['school'] == 'Not listed':
                    flash('Свържете се с Вашия директор, за да регистрира училището Ви или се свържете с нас по телефона - <a href="tel:+359 988 329 931">+359 988 329 931</a>.', 'danger')
                    return my_redirect(url_for('login_register', type="School", action='register'))
                
                my_school = School.query.filter(School.name == school).one()
                
                insert_user(request.form['name'], request.form['email'], request.form['password'], school=my_school)
                
                session['email'] = request.form['email']
                session['company_id'] = my_school.id
                session['name'] = request.form['name']
                session['company'] = my_school.name
                session['type'] = 'Teacher'

                try:
                    if session['redirect']:
                        return my_redirect(session['redirect'])
                    else:
                        return my_redirect('/')
                except:
                    return my_redirect('/')
            else:
                if len(User.query.filter(User.email == request.form['email']).all()) != 0:
                    flash('User is already registered or passwords does not match.', 'danger')
                elif request.form['password'] != request.form['password-confirm']:
                    flash('Please, just log in.', 'info')
                return my_redirect(url_for('login_register', type="Company", action='register'))
        else:
            if (request.form['password'] == request.form['password-confirm'])\
                    and (len(User.query.filter(User.email == request.form['email']).all()) == 0):

                if request.form['company'] == 'Not listed':
                    flash('Invalid comapny.', 'danger')
                    return my_redirect(url_for('login_register', type="Company", action='register'))
                
                my_company = {}

                if Company.query.filter(Company.name == request.form['company']).count() == 1:
                    my_company = Company.query.filter(Company.name == request.form['company']).one()
                else:
                    my_company = insert_company(request.form['company'])
                print('', my_company.name, my_company.id, my_company.uid)
                insert_user(request.form['name'], request.form['email'],
                            request.form['password'], company = my_company)

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
                if len(User.query.filter(User.email == request.form['email']).all()) != 0:
                    flash('User is already registered or passwords does not match.', 'danger')
                elif request.form['password'] != request.form['password-confirm']:
                    flash('Please, just log in.', 'info')
                return my_redirect(url_for('login_register', type="Company", action='register'))
    else:
        if 'email' in session and session['email'] is not None:
            return my_redirect('/')
        if len(request.form['email']) < 6:
            flash('Please, enter valid email address.', 'danger')
        if len(request.form['password']) < 8:
            flash('Please, enter a longer password.', 'info')
        if len(request.form['name']) < 3:
            flash('Please, enter a longer name.', 'info')
        return my_redirect(url_for('login_register', type="Company", action='register'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    if len(User.query.filter(User.email == request.form['email']).all()) == 1:
        user = User.query.filter(User.email == request.form['email']).one()

        if user.password_hash != crypto(request.form['password']):
            flash('Incorrect password.', 'danger')
            return my_redirect(url_for('login_register', action="login"))

        if (user.company_id is None or user.company_id == 'None') and (user.school_id is None or user.school_id == 'None'):
            session['email'] = request.form['email']
            session['name'] = User.query.filter(User.email == request.form['email']).all()[0].name
            session['id'] = User.query.filter(User.email == request.form['email']).all()[0].id
            session['company_id'] = None
            session['type'] = 'Student'
        elif user.company_id is None or user.company_id == 'None':
            session['email'] = request.form['email']
            session['school_id'] = user.school_id
            session['name'] = user.name
            session['school'] = user.school.name
            if user.id == user.school.admin:
                session['type'] = 'Director'
            else:
                session['type'] = 'Teacher'
        elif user.school_id is None or user.school_id == 'None':
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


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('core/' + str(session['language'] or get_locale()) + '/visitor/Forgoten-password.html')
    elif request.method == 'POST':
        user = User.query.filter(User.email == request.form['email']).one()
        from app.v1.mail_tools.mailer import Mailer
        Mailer.sendPasswordReset(user)
        flash('Check your inbox to reset your password.')
        return my_redirect('/')


@app.route('/reset/<verification>', methods=['GET', 'POST'])
def reset(verification):
    verify = Verify.query.filter(Verify.code == verification).one()
    user = verify.user[0]
    if request.method == 'GET':
        return render_template('user/reset.html', user=user)
    elif request.method =='POST':
        import sys
        print(request.form['password'], request.form['password-confirm'], file=sys.stderr, flush=True)
        print(User.query.filter(User.verification_id == verify.id).all(), file=sys.stderr, flush=True)
        if request.form['password'] == request.form['password-confirm']:
            User.query.filter(User.verification_id == verify.id).update({'password_hash': crypto(request.form['password'])})
            db.session.commit()
            return my_redirect(url_for('login_register'))
        else:
            flash('New password does not match.')
            return my_redirect('/reset/' + verification)


@app.route('/verify/<verification>')
def verify(verification):
    verify = Verify.query.filter(Verify.code == verification).one()
    user = User.query.filter(User.verification == verify).one()
    # import sys
    # print(user.__dict__, file=sys.stderr)
    # print(verify.__dict__, file=sys.stderr)
    session['email'] = user.email
    session['id'] = user.id
    session['company_id'] = user.company_id if user.company_id is not None else None
    session['type'] = 'Company' if user.company_id is not None else 'Student'
    session['name'] = user.name
    session['company'] = user.company.name if user.company_id is not None else None
    session['redirect'] = None
    session['language'] = get_locale()
    return redirect('/')


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
