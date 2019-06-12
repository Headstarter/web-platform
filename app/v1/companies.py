from app import render_template, flash, app
from app.router import my_redirect
from app.models import User, Tag, Company, Position, Application, insert_position, \
	update_position, db, filter_offers_by_tag, filter_applications, update_company
from flask import session, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = 'static/img/company/'


def allowed_image(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


class Companies:

	@staticmethod
	def upload_logo():
		from flask import jsonify
		if request.method == 'POST':
			# check if the post request has the file part
			if 'logo' not in request.files:
				return jsonify({'value': 'No logo field available.'}), 400
			file = request.files['logo']
			# if user does not select file, browser also
			# submit a empty part without filename
			if file.filename == '':
				flash('No selected file')
				return jsonify({'value': 'No file selected.'}), 400
			if file and allowed_image(file.filename):
				# filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['APP_ROOT'], Company.query.filter(Company.id == session['company_id']).one().logo[1:]))
				return jsonify({'value': 'Uploaded'}), 200

	@staticmethod
	def edit_company_profile():
		curr_company = Company.query.filter(Company.id == int(session['company_id'])).all()
		print(curr_company)
		if len(curr_company) != 1:
			flash('This offer not found.', 'info')
			return render_template("404.html"), 404
		
		curr_position = curr_company[0]
		
		import sys
		print('\n\n', curr_position, '\n\n')
		import sys
		print('\n\n' + str(dict(request.form)) + '\n\n')
		update_company(session['company_id'],
						request.form['company-name'],
						request.form['website'],
						request.form['description'])

		return my_redirect(url_for('core.list_my_offers'))
	
	@staticmethod
	def homepage():
		return render_template('core/' + str(session['language'] or get_locale()) + '/company/index.html',
								tags=Tag.query.all(),
								number_offers=Position.query.filter(Position.available == True).count(),
								open=[Position.query.filter(Position.available == True)
													.filter(Position.tag_id == x.id)
													.count() for x in Tag.query.all()],
								positions=Position.query.filter(Position.available == True)
														.order_by(Position.id.desc())
														.limit(5))

	@staticmethod
	def post_offer():
		if request.method == 'GET':
			return render_template('core/' + str(session['language'] or get_locale()) + '/company/post-offer.html', positionId=-1, tags=Tag.query.all())
		else:
			import sys
			print('\n\n' + str(dict(request.form)) + '\n\n')
			positionId = -1
			if request.form['id'] == '-1':
				positionId = insert_position(request.form['job-title'],
								request.form['email'],
								request.form['location'],
								session['company_id'],
								request.form['description'],
								True,
								request.form['duration'],
								request.form['job-type'],
								request.form['job-age'],
								request.form['job-category'])
			elif Position.query.filter(Position.id == int(request.form['id'])).count() == 1 and \
					Position.query.filter(Position.id == int(request.form['id'])).one().company_id == session['company_id']:
				positionId = update_position(
								request.form['id'],
								request.form['email'],
								request.form['location'],
								request.form['job-title'],
								session['company_id'],
								request.form['description'],
								True,
								request.form['duration'],
								request.form['job-type'],
								request.form['job-age'],
								request.form['job-category'])
			else:
				return render_template('404.html'), 404

			return my_redirect(url_for('core.list_my_offers'))
	
	@staticmethod
	def edit_offer(positionId):
		curr_position = Position.query.filter(Position.id == int(positionId)).all()
		
		if len(curr_position) != 1:
			flash('This offer not found.', 'info')
			return render_template("404.html"), 404
		
		curr_position = curr_position[0]
		
		if curr_position.company_id != session['company_id']:
			flash('This offer is not yours.', 'info')
			return render_template("404.html"), 404
		
		import sys
		print('\n\n', curr_position, '\n\n')
		if request.method == 'GET':
			return render_template('core/' + str(session['language'] or get_locale()) + '/company/post-offer.html', positionId=positionId, tags=Tag.query.all(), position=curr_position)
		else:
			import sys
			print('\n\n' + str(dict(request.form)) + '\n\n')
			positionId = update_position(
							positionId,
							request.form['email'],
							request.form['location'],
							request.form['job-title'],
							session['company_id'],
							request.form['description'],
							True,
							request.form['duration'],
							request.form['job-type'],
							request.form['job-age'],
							request.form['job-category'])

			return my_redirect(url_for('core.list_my_offers'))
	
	@staticmethod
	def list_my_offers():
		positions = []
		import sys
		print(request.form.get('tag'))
		print(request.args.get('tag'))
		if request.args.get('tag') and request.args['tag'] != '0':
			positions = filter_offers_by_tag(int(request.args['tag']), session['company_id'])
		else:
			positions = filter_offers_by_tag(company=session['company_id'])
		
		return render_template('core/' + str(session['language'] or get_locale()) + '/company/list_offers.html',
							   tags=Tag.query.all(),
							   positions=positions.all()
							   )
	
	@staticmethod
	def offer_details(id):
		try:
			return render_template('core/' + str(session['language'] or get_locale()) + '/company/offer-details.html',
								   recents=Position.query.filter(Position.available == True)
								   .order_by(Position.id.desc())
								   .limit(5).all()
								   ,
								   offer=Position.query.filter(Position.available == True)
								   .filter(Position.id == id).one())
		except:
			flash('This offer was not found.', "warn")
			return render_template("404.html"), 404
	
	@staticmethod
	def list_my_candidates():
		candidates = []
		import sys
		print(request.form.get('tag'))
		print(request.args.get('tag'))
		if request.args.get('tag') and request.args['tag'] != '0':
			candidates = filter_applications(int(request.args['tag']), session['company_id'])
		else:
			candidates = filter_applications(company=session['company_id'])
		
		# JUST TESTING = REMOVE BEFORE RELEASE
		if candidates.count() == 0:
			flash('Все още няма постъпили кандидати', 'info')
			
		return render_template('core/' + str(session['language'] or get_locale()) + '/company/list_candidates.html',
							   tags=Position.query.filter(Position.company_id == session['company_id']).all(),
							   candidates=candidates.all()
							   )
	
	@staticmethod
	def profile():
		company = Company.query.filter(Company.id == session['company_id']).one()
		return render_template('core/' + str(session['language'] or get_locale()) + '/company/profile.html', company=company)
#"""
#	@staticmethod
#	def create_offer():
#		id = insert_position('', session['company_id'], '', False, 0, 0, '', 1)
#		return redirect(url_for('v1pre_routes.position_view', positionId=id))
#
#	@staticmethod
#	def delete_offer(positionId):
#		import sys
#		print(positionId)
#		positionId=int(positionId)
#		print(Position.query.filter(Position.id == positionId).one().company_id)
#		print(session['company_id'])
#		if Position.query.filter(Position.id == positionId).one().company_id == session['company_id']:
#			Position.query.filter(Position.id == positionId).delete()
#			db.session.commit()
#			return redirect(url_for('v1pre_routes.my_offers'))
#		else:
#			flash("Access denied.", 'danger')
#			return render_template('template.html'), 401
#
#	@staticmethod
#	def browse_students():
#		page = int(request.args.get('page', default='0'))
#		offers_per_page = 10
#		position = -2
#
#		if request.form.get('position'):
#			position = int(request.form.get('position')) - 1
#
#		if position == -2:
#			applications = Application.query.filter(Application.company_id == int(session['company_id'])).all()
#			if len(applications) == 0:
#				flash('За момента няма кандидати за Вашите стажове.', 'info')
#			return render_template('company/browse_students.html',
#									positions=Position.query.filter(Position.company_id == int(session['company_id'])).order_by(Position.id.desc()),
#									students=applications)
#		else:
#			applications = Application.query.filter(Application.company_id == int(session['company_id']) and
#																	  Application.position_id == position)
#			if len(applications) == 0:
#				flash('За момента няма кандидати за Вашите стажове.', 'info')
#			return render_template('company/browse_students.html',
#									positions=Position.query.filter(Position.company_id == int(session['company_id'])).order_by(Position.id.desc()),
#									students=applications)
#
#	@staticmethod
#	def my_offers():
#		return render_template('company/my_offers.html',
#							   positions=Position.query.filter(Position.company_id == int(session['company_id'])).order_by(Position.id.desc()).all())
#
#	@staticmethod
#	def application_view(applicationId):
#		application = Application.query.filter(Application.id == applicationId).one()
#		if application.company_id != session['company_id']:
#			flash('Тази кандидатура не е по обява на Вашата фирма.', 'danger')
#			return render_template('template.html')
#		return render_template('company/application.html', application=application)
#
#	@staticmethod
#	def company_view(companyId):
#		company = Company.query.filter(Company.id == companyId)[0]
#		if companyId == session['company_id']:
#			return render_template('company/company.html', company=company)
#		else:
#			return render_template('students/company.html', company=company)
#
#	@staticmethod
#	def sector_view(sectorId):
#		return render_template('students/sector.html', sector=Sector.query.filter(Sector.id == sectorId)[0], companies=Company.query.filter(Company.sector_id == sectorId).all())
#
#	@staticmethod
#	def position_view(positionId):
#		position = Position.query.filter(Position.id == positionId)[0]
#		if position.company_id == session['company_id']:
#			return render_template('company/position.html', position=position, tags=Tag.query.all())
#		else:
#			return render_template('students/position.html', position=position, tags=Tag.query.all())
#
#	@staticmethod
#	def profile():
#		company = Company.query.filter(Company.id == session['company_id'])[0]
#		return render_template('company/profile.html', company=company)
#"""
#