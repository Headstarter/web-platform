from app import render_template, flash, app
from flask import session, request, url_for, redirect
from app.models import User, Tag, Company, Position, create_cv
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER_CV'] = 'static/img/cv/'


def allowed_image(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


class Students:

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
				destination = os.path.join(app.config['APP_ROOT'], User.query.filter(User.id == session['id']).one().cv.photo[1:])
				with open(destination, "a+") as f:
					# filename = secure_filename(file.filename)
					file.save(destination)
				return jsonify({'value': 'Uploaded'}), 200

	@staticmethod
	def company_view(companyId):
		company = Company.query.filter(Company.id == companyId)[0]
		return render_template('students/company.html', company=company)

	@staticmethod
	def sector_view(sectorId):
		return render_template('students/sector.html', sector=Sector.query.filter(Sector.id == sectorId)[0], companies=Company.query.filter(Company.sector_id == sectorId).all())

	@staticmethod
	def position_view(positionId):
		if len(Position.query.filter(Position.id == positionId).filter(Position.available == True).all()) == 0:
			flash('This position is not available.', 'danger')
			return render_template('template.html'), 404

		return render_template('students/position.html', tags=Tag.query.all(), position=Position.query.filter(Position.id == positionId).filter(Position.available == True).one())

	@staticmethod
	def profile():
		import sys
		student = User.query.filter(User.id == session['id'])[0]
		print(student.cv.get_education(), file=sys.stderr)
		return render_template('students/profile.html', student=student)

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

