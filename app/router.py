from app import app, babel, db, migrate, render_template
from app.models import Verify, insert_user, User, Tag, Company, Position, crypto, Mapper, insert_company
from flask import request, session, flash, redirect, url_for, send_file, Response
import sys

app.config['STATIC_FOLDER'] = '/static/wt_prod-20039'
app.secret_key = 'b94079a3717eda429c4580496be97bc9675d3ea4eb0ae50d'


def my_redirect(path):
    import flask
    response = flask.Response(response=redirect(path).data, status=200)
    response.headers['X-Response-URL'] = path
    return response


@babel.localeselector
def get_locale():
    translations = ['bg', 'en']
    return request.accept_languages.best_match(translations) or 'en'


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
        session['type'] = 'Visitor'

    print(request.full_path + ': ' + str(session) + ': ' + str(session))


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

import os
def get_sitekey():
    try:
        if os.environ['DEBUG'] == 'yes':
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

    print('\n\n\n\n', Company.query.all(), '\n\n\n\n\n\n')

    return render_template('core/' + str(session['language'] or get_locale()) + '/visitor/login-register.html', sitekey=get_sitekey(), action=action, type=type_user, companies=Company.query.all())


@app.route('/register', methods=['GET', 'POST'])
def register():
    print(request.form)
    member = 'off'
    try:
        member = request.form['member'] or 'off'
    except:
        member = 'off'
    
    if member == 'on':
        company = request.form['company']

    if len(request.form['email']) >= 6 and len(request.form['password']) >= 8 and len(request.form['name']) >= 3:
        if member != 'on':
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
                    flash('User is already registered or passwords does not match.', 'danger')
                elif request.form['password'] != request.form['password-confirm']:
                    flash('Please, just log in.', 'info')
                return my_redirect(url_for('login_register', type="Student", action='register'))
        else:
            if (request.form['password'] == request.form['password-confirm'])\
                    and (len(User.query.filter(User.email == request.form['email']).all()) == 0):

                my_company = {}

                if Mapper.query.filter(Mapper.company_name == request.form['company']).count() == 1:
                    print('\t\t\tMapper found')
                    my_company = Company.query.filter(Company.id == Mapper.query.filter(
                        Mapper.company_name == request.form['company']).one().company_id).one()
                else:
                    print('\t\t\tMapper NOT found')
                    my_company = insert_company(request.form['company'])
                print('', my_company.name, my_company.id, my_company.uid)
                insert_user(request.form['name'], request.form['email'],
                            request.form['password'], my_company)

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
        if session['email'] is not None:
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


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('')
    elif request.method == 'POST':
        user = User.query.filter(User.email == request.form['email']).one()
        from app.v1.helpers.mailer import Mailer
        return Mailer.sendPasswordReset(user)


@app.route('/reset/<verification>', methods=['GET', 'POST'])
def reset(verification):
    verify = Verify.query.filter(Verify.code == verification).one()
    user = verify.user
    if request.method =='GET':
        return render_template('user/reset.html', user=user)
    elif request.method =='POST':
        User.query.filter(User.id == user.id).update({'password_hash': crypto(request.form['password'])})
        db.session.commit()
        return redirect(url_for('login_register'))


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
