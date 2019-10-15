from app import render_template, flash, app
from app.router import my_redirect
from flask import session, request, url_for, redirect
from app.models import User, Tag, Company, Position, create_cv, update_cv, CV
import os
from werkzeug.utils import secure_filename
from app.v1.target import Target_Group, abstractmethod


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER_CV'] = 'static/img/cv/'


def allowed_image(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


class Students:
	@staticmethod
	def homepage():
		return render_template('core/' + str(session['language'] or get_locale()) + '/students/index.html',
								tags=Tag.query.all(),
								number_offers=Position.query.filter(
									Position.available == True).count(),
								open=Target_Group.groupTags(),
								positions=Position.query.filter(
									Position.available == True)
								.order_by(Position.id.desc())
								.limit(5))


	@staticmethod
	def upload_cv_picture():
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
				import os
				saved = False
				where = 'static/wt_prod-20039/images/students/' + str(User.query.filter(User.id == session['id']).one().id) + '.png'
				where_db = '/images/students/' + str(User.query.filter(User.id == session['id']).one().id) + '.png'
				where = os.path.join(os.environ['basedir'], where)
				os.system('echo > ' + where)
				with open(where, 'a'):
					os.utime(where, None)
				while not saved:
					import sys
					try:
						file.save(where)
						saved = True
						print('Saved', file=sys.stderr)
					except FileNotFoundError:
						print('FileNotFound', file=sys.stderr)
						import shutil
						shutil.copy(os.path.join(os.environ['basedir'], 'static/wt_prod-20039/images/students/150.png'), 
                  					where)
					except TypeError:
						import sys
						print('TypeError', file=sys.stderr)
						cv_id = User.query.filter(User.id == session['id']).one().cv_id
						print('cv_id', cv_id, file=sys.stderr)
						CV.query.filter(CV.id == cv_id).update({'photo': where_db});
						db.session.commit()

				return jsonify({'value': 'Uploaded'}), 200
	
	@staticmethod
	def edit_student_profile():
		curr_user = User.query.filter(User.id == int(session['id'])).all()
		print(curr_user)
		if len(curr_user) != 1:
			flash('This offer not found.', 'info')
			return render_template("404.html"), 404
		
		curr_user = curr_user[0]
		
		import sys
		print('\n\n', curr_user, '\n\n')
		import sys
		print('\n\n' + str(dict(request.form)) + '\n\n')
		import json
		print('\n\n' + str(request.__dict__) + '\n\n')
		
		x = update_cv(session['id'],
				request.form['name'],
				request.form['email'],
				request.form['telephone'],
				request.form['location'],
				request.form['birthday'],
				request.form['languages'],
				request.form['education'],
				request.form['projects'],
				request.form['resume-content'],
				request.form['skills'],
				request.form['hobbies'])
		print('\n\n' + str(x) + '\n\n')
		
		return my_redirect(url_for('core.profile'))
		
	@staticmethod
	def profile():
		import sys
		student = User.query.filter(User.id == session['id']).one()
		try:
			print(student.cv.get_education())
		except:
			create_cv(student)
		student = User.query.filter(User.id == session['id']).one()
		return render_template('core/' + str(session['language'] or get_locale()) + '/students/edit_cv.html', student=student)

	@staticmethod
	def cv_confirm():
		try:
			# return str(session['redirect'])
			if request.args['cv_confirmed'] == '1':
				return redirect(session['redirect'])
		except:
			pass
		student = User.query.filter(User.id == session['id'])[0]
		return render_template('visitor/profileView.html', student=student, current=request.full_path, confirm=url_for('v1pre_routes.profile',
																							studentId=session['id']))
	
	@staticmethod
	def offer_details(id):
		try:
			return render_template('core/' + str(session['language'] or get_locale()) + '/visitor/offer-details.html',
								   recents=Position.query.filter(Position.available == True)
								   .order_by(Position.id.desc())
								   .limit(5).all()
								   ,
								   offer=Position.query.filter(Position.available == True)
								   .filter(Position.id == id).one())
		except:
			flash('This offer was not found.', "warn")
			return render_template("404.html"), 404
