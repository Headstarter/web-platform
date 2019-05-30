from app import app, babel, db, migrate, render_template
from app.router import session
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
	return render_template('core/visitor/faq.html')


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
	return mapped_routes[session['type']].offer_details(position_id)

# @routes.route('/cv/<user_id>')
# def profile_view(user_id):
#     return mapped_routes['Visitor'].profile_view(user_id)


@routes.route('/profile')
def profile():
	return mapped_routes[session['type']].profile()


@routes.route('/cv/<int:id>')
def profileView(id):
	return mapped_routes[session['type']].profile()


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
		return render_template('core/students/template.html')


@routes.route('/about')
def about():
	return render_template('core/visitor/about.html')


@routes.route('/upload/cv/picture', methods=['POST'])
def upload_cv_picture():
	if session['type'] == 'Student':
		return mapped_routes['Student'].upload_cv_picture()
	else:
		flash('В момента нямате достъп до тази страница. Моля, опитайте да влезете в системата.', 'warning')
		flash('<a class="nav-link" href="#" data-toggle="modal" data-target="#student_company">Вход</a>', 'info')
		session['redirect'] = url_for('v1pre_routes.upload_logo')
		return render_template('template.html')

#
# @routes.route('/apply/<position>')
# def apply_students(position):
#     return mapped_routes['Visitor'].apply_student(position)
#
#
# @routes.route('/profile')
# def profile():
#     try:
#         return mapped_routes[session['type']].profile()
#     except:
#         try:
#             return mapped_routes['Visitor'].profile()
#         except:
#             flash('В момента нямате достъп до тази страница. Моля, опитайте да влезете в системата.', 'warning')
#             flash('<a class="nav-link" href="#" data-toggle="modal" data-target="#student_company">Вход</a>', 'info')
#             session['redirect'] = url_for('v1pre_routes.profile')
#             return render_template('template.html')
#
#
# @routes.route('/cv/confirm')
# def cv_confirm():
#     try:
#         return mapped_routes[session['type']].cv_confirm()
#     except:
#         flash('В момента нямате достъп до тази страница. Моля, опитайте да влезете в системата.', 'warning')
#         flash('<a class="nav-link" href="#" data-toggle="modal" data-target="#student_company">Вход</a>', 'info')
#         session['redirect'] = url_for('v1pre_routes.profile')
#         return render_template('template.html')
#
#
# @routes.route('/profile/<studentId>/view')
# def profileView(studentId):
#     try:
#         return mapped_routes['Visitor'].profile_view(studentId)
#     except:
#         flash('В момента нямате достъп до тази страница. Моля, опитайте да влезете в системата.', 'warning')
#         flash('<a class="nav-link" href="#" data-toggle="modal" data-target="#student_company">Вход</a>', 'info')
#         session['redirect'] = url_for('core.profile')
#         return render_template('template.html')
#
#
# @routes.route('/company/<int:companyId>', methods=['GET', 'POST'])
# def company_view(companyId):
# 	return mapped_routes['Visitor'].company_view(companyId)
#
#
# @routes.route('/application/<applicationId>', methods=['GET', 'POST'])
# def application_view(applicationId):
#     try:
#         return mapped_routes[session['type']].application_view(applicationId)
#     except:
#         flash('В момента нямате достъп до тази страница. Моля, опитайте да влезете в системата.', 'warning')
#         flash('<a class="nav-link" href="#" data-toggle="modal" data-target="#student_company">Вход</a>', 'info')
#         session['redirect'] = url_for('v1pre_routes.application_view', applicationId=applicationId)
#         return render_template('template.html')
