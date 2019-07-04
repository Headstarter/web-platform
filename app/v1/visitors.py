from app import render_template, flash
from flask import session
from flask import request, redirect, url_for
from app.models import User, Company, Position, Tag, Application, insert_application, create_cv, filter_offers_by_tag
import sys
from app.v1.target import Target_Group, abstractmethod

class Visitors:
	@staticmethod
	def folder():
		return 'visitor'

	@staticmethod
	def homepage():
		return render_template('core/' + str(session['language'] or get_locale()) + '/' + Visitors.folder() + '/index.html',
                        tags=Tag.query.all(),
                        number_offers=Position.query.filter(Position.available == True).count(),
                        open=Target_Group.groupTags(),
                        positions=Position.query.filter(Position.available == True)
                                                .order_by(Position.id.desc())
                                                .limit(5))

	@staticmethod
	def offer_details(id):
		try:
			return render_template('core/' + str(session['language'] or get_locale()) + '/' + Visitors.folder() + '/offer-details.html',
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
	def browse():
		positions = []
		import sys
		print(request.args.get('tag'))
		print(request.args.get('company'))
		company = request.args.get('company') or '0'
		tag = request.args.get('tag') or '0'
		group = request.args.get('group') or '-1'
		if group == '-1':
			if company == '0' and tag == '0':
				positions = filter_offers_by_tag()
			elif company == '0' and tag != '0':
				positions = filter_offers_by_tag(int(tag))
			elif tag == '0' and company != '0':
				positions = filter_offers_by_tag(company=int(company))
		else:
			positions = filter_offers_by_tag(group=int(group))
		
		return render_template('core/' + str(session['language'] or get_locale()) + '/visitor/browse.html',
							   tags=Tag.query.all(),
							   companies=Company.query.all(),
							   positions=positions,
							   company_selected=int(company),
							   tag_selected=int(tag),
							   )

	@staticmethod
	def profile():
		session['redirect'] = request.full_path
		session.modified = True
		return redirect(url_for('login_register', type="Student"))

	@staticmethod
	def random_cv(id):
		import sys
		student = User.query.filter(User.id == id)[0]
				
		return render_template('core/' + str(session['language'] or get_locale()) + '/visitor/profileView.html', student=student)
