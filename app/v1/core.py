from app import app, babel, db, migrate, render_template
from app.router import session, get_locale
from app.models import User, Tag, Company, Position, CV, insert_application
from flask import g, request, Blueprint, flash, url_for, redirect

from app.v1.visitors import Visitors
from app.v1.students import Students
from app.v1.companies import Companies

mapped_routes = {
    'Visitor': Visitors,
    'Student': Students,
    'Company': Companies
}

routes = Blueprint('core', __name__)


@routes.route('/browse', methods=['GET', 'POST'])
def browse():
    if session['type'] != 'Company':
        return mapped_routes['Visitor'].browse()
    else:
        session['redirect'] = request.full_path
        session.modified = True
        return redirect(url_for('login_register', type="Student"))


@routes.route('/school/register')
@routes.route('/school/register/')
@routes.route('/school/register/<step>')
def school_register(step="1"):
	import sys
	print("step: ", step, "!", file=sys.stderr)
	if step == '1':  # registration/login
		session['redirect'] = '/school/register/2'
		from app import login_register
		return login_register(type='School-Director')
	elif step == '2': # school registration form
		try:
			assert session['type'] != 'School-Director'
		except:
			session['redirect'] = '/school/register/2'
			from app import login_register
			return login_register(type='School-Director')
		return "" # school registration form
	else:
		return "" # unknown step


@routes.route('/')
@routes.route('/p')
def _homepage():
    try:
        return mapped_routes[session['type']].homepage()
    except AttributeError:
        return mapped_routes['Visitor'].homepage()


@routes.route('/internships/new', methods=['GET', 'POST'])
def post_offer():
    if session['type'] == 'Company':
        return mapped_routes[session['type']].post_offer()
    else:
        session['redirect'] = request.full_path
        session.modified = True
        return redirect(url_for('login_register', type="Company"))


@routes.route('/offer/<positionId>/edit', methods=['GET', 'POST'])
def edit_offer(positionId):
    if session['type'] == 'Company':
        return mapped_routes[session['type']].edit_offer(positionId)
    else:
        session['redirect'] = request.full_path
        session.modified = True
        return redirect(url_for('login_register', type="Company"))


@routes.route('/internships/my')
def list_my_offers():
    if session['type'] == 'Company':
        return mapped_routes[session['type']].list_my_offers()
    else:
        session['redirect'] = request.full_path
        session.modified = True
        return redirect(url_for('login_register', type="Company"))


@routes.route('/faq')
def faq():
    return render_template('core/' + str(session['language'] or get_locale()) + '/visitor/faq.html')


@routes.route('/news')
def news():
    return render_template('core/' + str(session['language'] or get_locale()) + '/visitor/news.html')


@routes.route('/videos/<id>')
def videos(id):
    if str(id) == "0":
        return redirect("http://news.bnt.bg/bg/a/mladezhi-spechelikha-sstezanie-s-platforma-za-namirane-na-stazh#")
    elif str(id) == "1":
        return redirect("https://www.bloombergtv.bg/update/2019-06-02/kakvi-vazmozhnosti-pred-uchenitsite-i-biznesa-dava-programata-teenovator")


@routes.route('/post/<id>')
def posts(id):
    if str(id) == "1":
        return render_template('core/' + str(session['language'] or get_locale()) + '/visitor/how_to_cv.html')
    elif str(id) == "2":
        return render_template('core/' + str(session['language'] or get_locale()) + '/visitor/how_to_hire.html')


@routes.route('/candidates/my')
def list_my_candidates():
    if session['type'] == 'Company':
        return mapped_routes[session['type']].list_my_candidates()
    else:
        session['redirect'] = request.full_path
        session.modified = True
        return redirect(url_for('login_register', type="Company"))


@routes.route('/internship/<position_id>')
def offer_view(position_id):
    views = Position.query.filter(Position.id == position_id).one().views
    Position.query.filter(Position.id == position_id).update(
        {"views": views + 1})
    return mapped_routes[session['type']].offer_details(position_id)


@routes.route('/profile')
def profile():
    return mapped_routes[session['type']].profile()


@routes.route('/cv/<int:id>')
def profileView(id):
    return mapped_routes['Visitor'].random_cv(id)


@routes.route('/company/<int:id>')
def company_view(id):
    return mapped_routes['Visitor'].company_view(id)


@routes.route('/company/profile/edit', methods=['POST'])
def edit_company_profile():
    if session['type'] == 'Company':
        return mapped_routes[session['type']].edit_company_profile()
    else:
        session['redirect'] = request.full_path
        session.modified = True
        return redirect(url_for('login_register', type="Company"))


@routes.route('/student/profile/edit', methods=['POST'])
def edit_student_profile():
    if session['type'] == 'Student':
        return mapped_routes[session['type']].edit_student_profile()
    else:
        session['redirect'] = request.full_path
        session.modified = True
        return redirect(url_for('login_register', type="Student"))


@routes.route('/upload/logo', methods=['POST'])
def upload_logo():
    if session['type'] == 'Company':
        return mapped_routes['Company'].upload_logo()
    else:
        flash('В момента нямате достъп до тази страница. Моля, опитайте да влезете в системата.', 'warning')
        flash('<a class="nav-link" href="#" data-toggle="modal" data-target="#student_company">Вход</a>', 'info')
        session['redirect'] = url_for('v1pre_routes.upload_logo')
        return render_template('template.html')


@routes.route('/candidate/<positionId>')
def candidate(positionId):
    if session['type'] != 'Student':
        session['redirect'] = request.full_path
        session.modified = True
        return redirect(url_for('login_register', type="Student"))
    else:
        insert_application(session['id'], int(positionId))
        flash('Подадохте си CV-то успешно.', 'success')
        return render_template('core/' + str(session['language'] or get_locale()) + '/students/template.html')


@routes.route('/about')
def about():
    return render_template('core/' + str(session['language'] or get_locale()) + '/visitor/about.html')


@routes.route('/upload/cv/picture', methods=['POST'])
def upload_cv_picture():
    if session['type'] == 'Student':
        return mapped_routes['Student'].upload_cv_picture()
    else:
        flash('В момента нямате достъп до тази страница. Моля, опитайте да влезете в системата.', 'warning')
        flash('<a class="nav-link" href="#" data-toggle="modal" data-target="#student_company">Вход</a>', 'info')
        session['redirect'] = url_for('v1pre_routes.upload_logo')
        return render_template('template.html')
