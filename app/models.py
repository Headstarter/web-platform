from app import db
import json


class Tag(db.Model):
	__tablename__ = 'Tag'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128))
	positions = db.relationship("Position", back_populates="tag")

	def __repr__(self):
		return '<Tag ' + str(self.id) + ' - ' + str(self.name) + '>'


class Company(db.Model):
	__tablename__ = 'Company'
	id = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer)

	employees = db.relationship("User", back_populates="company")
	positions = db.relationship("Position", back_populates="company")

	name = db.Column(db.String(128), unique=True)
	description = db.Column(db.String(32768))
	logo = db.Column(db.String(256))
	website = db.Column(db.String(256))
	contacts = db.Column(db.String(32768))

	def __repr__(self):
		return '<Company {}>'.format(self.name)


class User(db.Model):
	__tablename__ = 'User'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))

	cv_id = db.Column(db.Integer, db.ForeignKey('CV.id'), nullable=True)
	cv = db.relationship('CV', back_populates='user', uselist=False)

	company_id = db.Column(db.Integer, db.ForeignKey('Company.id'), nullable=True)
	company = db.relationship('Company', back_populates='employees')

	applications = db.relationship("Application", back_populates="user")

	def to_dict(self):
		return {"id": self.id,
				"name": self.name,
				"email": self.email,
				"company": self.company
			   }

	def __repr__(self):
		return '<User {}>'.format(self.name)


class CV(db.Model):
	__tablename__ = 'CV'

	id = db.Column(db.Integer, primary_key=True)

	user = db.relationship("User", back_populates="cv")

	photo = db.Column(db.String(256))
	name = db.Column(db.String(256))
	email = db.Column(db.String(256))
	telephone = db.Column(db.String(16))
	birthday = db.Column(db.String(256))
	# age = db.Column(db.String(16))
	location = db.Column(db.String(256))
	about = db.Column(db.String(512))
	# achievements

	education = db.Column(db.String(2048))
	projects = db.Column(db.String(2048))
	skills = db.Column(db.String(512))
	languages = db.Column(db.String(512))
	hobbies = db.Column(db.String(512))

	def get_skills(self):
		return json.loads(self.skills)

	def get_projects(self):
		return json.loads(self.projects)

	def get_education(self):
		return json.loads(self.education)

	def get_languages(self):
		return json.loads(self.languages)

	def get_hobbies(self):
		return json.loads(self.hobbies)

	def __repr__(self):
		return '<CV {}>'.format(self.name)

import datetime as DT

class Position(db.Model):
	__tablename__ = 'Position'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64))
	company_id = db.Column(db.Integer, db.ForeignKey('Company.id'))
	company = db.relationship('Company', back_populates='positions')
	description = db.Column(db.String(32768))
	location = db.Column(db.String(32768))
	date = db.Column(db.String(32768))
	available = db.Column(db.Boolean)
	duration = db.Column(db.Integer)
	email = db.Column(db.String(128))
	hours_per_day = db.Column(db.String(128))
	age_required = db.Column(db.String(128))
	tag_id = db.Column(db.Integer, db.ForeignKey('Tag.id'))
	tag = db.relationship('Tag', back_populates='positions')
	applications = db.relationship("Application", back_populates="position")
	
	def get_type(self):
		if self.hours_per_day == 'До 4ч.':
			return "Part Time<br><small>До 4 ч./ден</small>"
		if self.hours_per_day == '4-7ч.':
			return "Part Time<br><small>Между 4 и 7 ч./ден</small>"
		if self.hours_per_day == '8ч.':
			return "Full Time<br><small>8 ч./ден</small>"

	def get_full_date(self):
		posted = DT.datetime.strptime(self.date, '%Y-%m-%d %H:%M:%S.%f')
		return DT.datetime.strftime(posted, '%H:%M:%S %d-%m-%Y')
	
	def get_date(self):
		today = DT.datetime.today()
		posted = DT.datetime.strptime(self.date, '%Y-%m-%d %H:%M:%S.%f')
		if today - DT.timedelta(hours=1) < posted:
			return "{} minutes ago".format(int((today - posted).total_seconds() / 60.0))
		if today - DT.timedelta(hours=24) < posted:
			return "{} hours ago".format(int((today - posted).total_seconds() / 60.0 / 60.0))
		if today - DT.timedelta(days=7) < posted:
			return "{} days ago".format(int((today - posted).total_seconds() / 60.0 / 60.0 / 24.0))


class Application (db.Model):
	__tablename__ = 'Application'
	id = db.Column(db.String(2048), nullable=False, unique=True)
	user_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
	user = db.relationship('User', back_populates='applications')
	position_id = db.Column(db.Integer, db.ForeignKey('Position.id'), primary_key=True)
	position = db.relationship('Position', back_populates='applications')
	company_id = db.Column(db.Integer, primary_key=True)


import hashlib
import uuid


def gen_uid():
	return str(uuid.uuid4())


def crypto(password):
	return hashlib.sha256(bytes(password, 'utf-8')).hexdigest()


def clear():
	User.query.filter(True).delete()
	Company.query.filter(True).delete()
	Tag.query.filter(True).delete()
	Position.query.filter(True).delete()


def create_cv(student):
	cv = CV(photo='/static/img/cv/' + str(student.id) + '.jpg',
			name='',
			email='',
			birthday='',
			telephone='',
			location='',
			about='',
			education='[]',
			projects='[]',
			skills='[]',
			languages='[]',
			hobbies='[]'
			)
	db.session.add(cv)
	User.query.filter(User.id == student.id).update({'cv_id': cv.id})
	db.session.commit()


def insert_user(name, email, password, company=None):
	if company is None:
		db.session.add(User(name=name, cv=CV(photo='/static/img/cv/' + str(email) + '.jpg',
											 name='',
											 email='',
											 birthday='',
											 telephone='',
											 location='',
											 about='',
											 education='[]',
											 projects='[]',
											 skills='[]',
											 languages='[]',
											 hobbies='[]'
											 ), company=company, email=email, password_hash=crypto(password)))
	else:
		db.session.add(User(name=name, cv=None, company=company, email=email, password_hash=crypto(password)))
	db.session.commit()


def insert_application(user_id, position_id, company_id):
	db.session.add(Application(id=str(user_id)+'_'+str(position_id), user_id=user_id, position_id=position_id, company_id=company_id))
	db.session.commit()


def insert_position(name, email, location, company_id, description, available, duration, hours_per_day, age_required, tag_id):
	p = Position(
		name=name,
		email=email,
		location=location,
		company_id=company_id,
		description=description,
		available=available,
		duration=duration,
		hours_per_day=hours_per_day,
		age_required=age_required,
		tag_id=tag_id,
		date='{}'.format(DT.datetime.now())
	)
	db.session.add(p)
	db.session.commit()
	return p.id


def update_position(position_id, email, location, name, company_id, description, available, duration, hours_per_day, age_required, tag_id):
	Position.query.filter(Position.id == position_id).update({
		'name': name,
		'email': email,
		'location': location,
		'company_id': company_id,
		'description': description,
		'duration': duration,
		'hours_per_day': hours_per_day,
		'age_required': age_required,
		'tag_id': tag_id
	})
	db.session.commit()
	return position_id


def update_company(company_id, name, website, description):
	Company.query.filter(Company.id == company_id).update({
		'name': name,
		'website': website,
		'description': description
	})
	db.session.commit()
	return company_id


def activate_position(position_id):
	Position.query.filter(Position.id == position_id).update({
		available: True
	})
	db.session.commit()
	return position_id


def deactivate_position(position_id):
	Position.query.filter(Position.id == position_id).update({
		available: True
	})
	db.session.commit()
	return position_id


def filter_applications(position=None, company=None):
	if position is None:
		applications = Application.query
	else:
		applications = Application.query.filter(Application.position_id == position)
	if company is None:
		applications = applications
	else:
		applications = applications.filter(Application.company_id == company)
	return applications


def filter_offers_by_tag(position=None, company=None):
	if position is None:
		positions = Position.query.filter(Position.available == True)
	
	elif position == 1:
		positions = Position.query.filter(Position.available == True) \
			.filter(Position.tag_id <= 9)
	
	elif position == 10:
		positions = Position.query.filter(Position.available == True) \
			.filter(Position.tag_id > 9) \
			.filter(Position.tag_id <= 14)
	
	elif position == 15:
		positions = Position.query.filter(Position.available == True) \
			.filter(Position.tag_id > 14) \
			.filter(Position.tag_id <= 21)
	
	elif position == 22:
		positions = Position.query.filter(Position.available == True) \
			.filter(Position.tag_id > 21) \
			.filter(Position.tag_id <= 28)
	
	elif position == 29:
		positions = Position.query.filter(Position.available == True) \
			.filter(Position.tag_id > 28) \
			.filter(Position.tag_id <= 32)
	else:
		positions = Position.query.filter(Position.available == True)
		
	if company is not None:
		positions = positions.filter(Position.company_id == company)
	
	return positions.order_by(Position.id.desc())
	

def init():
	""" Tag """
	tags = [
		'Software Engineer', '&nbsp;&nbsp;&nbsp; Mobile Developer', '&nbsp;&nbsp;&nbsp; Frontend Developer', '&nbsp;&nbsp;&nbsp; Backend Developer', '&nbsp;&nbsp;&nbsp; Full-Stack Developer', '&nbsp;&nbsp;&nbsp; Engineering Manager', '&nbsp;&nbsp;&nbsp; QA Engineer', '&nbsp;&nbsp;&nbsp; DevOps', '&nbsp;&nbsp;&nbsp; Software Architect', 'Designer', '&nbsp;&nbsp;&nbsp; UI/UX Designer', '&nbsp;&nbsp;&nbsp; User Researcher', '&nbsp;&nbsp;&nbsp; Visual Designer', '&nbsp;&nbsp;&nbsp; Creative Director', 'Operations', '&nbsp;&nbsp;&nbsp; Finance/Accounting', '&nbsp;&nbsp;&nbsp; H.R.', '&nbsp;&nbsp;&nbsp; Office Manager', '&nbsp;&nbsp;&nbsp; Recruiter', '&nbsp;&nbsp;&nbsp; Customer Service', '&nbsp;&nbsp;&nbsp; Operations Manager', 'Sales', '&nbsp;&nbsp;&nbsp; Business Development', '&nbsp;&nbsp;&nbsp; Sales Development', '&nbsp;&nbsp;&nbsp; Account Executive', '&nbsp;&nbsp;&nbsp; BD Manager', '&nbsp;&nbsp;&nbsp; Account Manager', '&nbsp;&nbsp;&nbsp; Sales Manager', 'Marketing', '&nbsp;&nbsp;&nbsp; Growth Hacker', '&nbsp;&nbsp;&nbsp; Marketing Manager', '&nbsp;&nbsp;&nbsp; Content Creator', 'Hardware Engineer', 'Mechanical Engineer', 'Systems Engineer', 'Business Analyst', 'Data Scientist', 'Product Manager', 'Project Manager'#, 'Attorney', '&nbsp;&nbsp;&nbsp; CEO', '&nbsp;&nbsp;&nbsp; CFO', '&nbsp;&nbsp;&nbsp; CMO', '&nbsp;&nbsp;&nbsp; COO', '&nbsp;&nbsp;&nbsp; CTO'
	]
	Tags_db = []
	for x in tags:
		tag = Tag(name=x)
		db.session.add(tag)
		db.session.commit()
		print(Tag.query.get(len(Tags_db) + 1), end=' ')
		Tags_db.append(Tag.query.get(len(Tags_db) + 1))
	print()

	""" Companies """
	# Headstarter = Company(name='Headstarter', website='https://headstarter.eu',
	# 					  contacts='Mail Us: contact@headstarter.eu', logo='/static/img/company/1.png',
	# 					  description='We are connecting students and business.', uid="f1d6d91e-affc-4141-9cf8-ccf16e082b56")
	# db.session.add(Headstarter)
	# db.session.commit()

	# Biodit = Company(name='Biodit Global Technologies', website='https://biodit.com',
	# 				 contacts="""
	# 				 Visit Us: бул. „св. Климент Охридски“ 125, 1756 кв. Малинова долина, София<br>
	# 				 Mail Us: pr@biodit.com, office@biodit.com""", logo='/static/img/company/2.png',
	# 				 description='Example of description', uid="da39ec10-7eba-4325-907e-40aa38d76c22")
	# db.session.add(Biodit)
	# db.session.commit()

	# Deamix = Company(name='Dreamix', website='',
	# 				 contacts="", logo='/static/img/company/3.png',
	# 				 description='', uid="8f4aaa61-eba2-4578-b0ed-f1738088b4b0")

	# BICA_services = Company(name='BICA services', website='',
	# 				 contacts="", logo='/static/img/company/4.png',
	# 				 description='', uid="fe639fe8-5028-44c7-bfc6-185e557cc32b")

	# iGreet = Company(name='iGreet', website='',
	# 				 contacts="", logo='/static/img/company/5.png',
	#				 description='', uid="299b9e13-a34f-4c04-bc72-1f3bc72a92b8")

	# db.session.add(Deamix)
	# db.session.add(BICA_services)
	# db.session.add(iGreet)
	# db.session.commit()
	
	index = 1
	companies = ['Headstarter', 'Axway', 'Biodit', 'Codix', 'DoITwise', 'ДЗИ', 'ОББ', 'HP', 'IT hub Kaufland', 'Nestle', 'Paraflow']
	uids = ['4c716bc2-40c9-467e-9474-11f61d40d0ae', 'c2d952d8-7b14-4aeb-b49d-f9e1a45d4aad', 'cfdfa522-a0f1-43f8-bc60-eca0c9baf3f6', 'a3c3eed4-08bf-44fa-8238-c4df7d88ffc0', '2d479f9e-c75e-4a5d-9a8a-aeb7af9ea8f1', 'a86bb922-c025-4921-9e04-e0b54fb76e14', '0609133d-13d1-45ba-b524-c87e60466a09', '4c6e0b7f-d819-4c10-be26-65ba9934398b', 'b3991016-f948-4b2b-b178-202e2c100439', 'e41a9dc3-b44c-4a05-bbce-c816578e2b60', 'f397ec8f-dc2d-4df5-bf46-ada57bb02cf8']
	for company in companies:
		curr_company = Company(name=company, website='',
					 contacts="", logo='/static/img/company/' + str(index) + '.png',
					 description='', uid=uids[index - 1])
		print(company, gen_uid())
		db.session.add(curr_company)
	db.session.commit()

	""" CEOs """
	# insert_user(name='Alex Tsvetanov', company=Headstarter, email='alex@alexts.tk', password=crypto('password'))

	""" Positions """
	# example1 = Position(name='Python Web Developer', company=Headstarter,
	# 				   description="<strong>Пробно</strong> <i>описание</i> на <u>стажанстка програма</u>",
	# 				   available=True, duration=3, hours_per_day="7-8ч.",
	# 				   age_required='Поне 16 г.', tag=Tags_db[3], email="headstarter@headstarter.eu", location="Някъде", date='{}'.format(DT.datetime.now()))
	# db.session.add(example1)
	# db.session.commit()

	# example2 = Position(name='C/C++ Back-end Developer', company=Headstarter, email="headstarter@headstarter.eu",
# 					   description="""
# Takeaway.com is Europe’s leading online and mobile food ordering company, dedicated to connecting consumers with their favorite local restaurants. The people who work at Takeaway.com are our company's greatest asset; each person at Takeaway.com plays an integral part in building tools and technology that help connect and transact our consumers and restaurants - at scale.<br>
# <br>
# The company’s online and mobile ordering platforms allow meals to order directly from more than 40,000 takeout restaurants all over Europe and beyond. The Takeaway.com portfolio of brands includes Takeaway.com, Thuisbezorgd.nl, Lieferando.de, Pyszne.pl, Lieferservice.at and Vietnammm.com. The working atmosphere at Takeaway.com is characterized by team spirit,
# trust and open communication as well as a high degree of personal responsibility. Bringing in your own ideas is encouraged and creativity, motivation and commitment are much appreciated.<br>
# <br>
# The Position: <br>
# <br>
# We are looking for talented Front-End Developers to join our multinational and multicultural IT organization. You will play a key role in helping on our journey towards high performance teams following agile values and principles.<br>
# <br>
# Your Profile: <br>
# <br>
# ● At least 3 years of professional experience<br>
# ● Excellent knowledge of HTML 5, CSS 3 and DOM<br>
# ● In-depth knowledge of JavaScript(ECMAScript 5)<br>
# ● Experience with frameworks for front-end development - Angular, React, Vue.js, etc<br>
# ● Knowledge of template engines - Smarty, Twig, Blade, Razor, etc<br>
# ● Experience in processing web pages on different platforms<br>
# ● Working with Related Micro Services and(RESTful) APIs<br>
# ● Practice with Test Driven Development, using device testing technologies<br>
# ● Experience with code versioning( especially Git ) <br>
# <br>
# Advantages : <br>
# <br>
# ● Understanding of the work of the HTTP protocol<br>
# ● Experience with Vue.js<br>
# ● Work with Node.js or Dart<br>
# ● Experience with Blade Template Engine(Laravel)<br>
# ● Familiarity or experience with ECMAScript 6 in JavaScript<br>
# ● Familiarity or experience with TypeScript<br>
# ● Task trainer experience - Grunt, Gulp, etc.<br>
# ● Familiarity or experience with Webpack and / or Laravel-mix<br>
# ● Knowledge of CSS preprocessors -LESS, SASS<br>
# ● Experience with Bootstrap framework<br>
# ● Experience with Test Driven Development, using device testing technologies<br>
# ● Experience or familiarity with the Scrum methodology<br>
# <br>
# What We offer? <br>
# <br>
# ● A place where your ideas are heard and where you can really grow and learn with your team.<br>
# ● A more than competitive salary with(long term) incentives in accordance with your experience.<br>
# ● Awesome teams and people, in a fast growing company.<br>
# ● Being part of a young, professional and truly international team.<br>
# ● The opportunity to learn new concepts and practice them in a safe environment.<br>
# ● The freedom to go where no one in our company has gone before.<br>
# ● Free drinks, fruit, several sports benefits and regular awesome team events<br>
# <br>
# Takeaway offers career advancement and lucrative compensation. The Technology department has regular knowledge sharing, training and attends/speaks at global conferences<br>
# <br>
# How to apply?<br>
# <br>
# If you are interested, follow the link below and please send us your CV / Resume.<br>
# We will read all the information on it and we will contact the most suitable candidates.<br>
# Your personal data is protected by Bulgarian law and European General Data Protection Regulation.<br>
# """,
# 					   available=True, duration=6, hours_per_day="До 4ч.",
# 					   age_required='Поне 16 г.', tag=Tags_db[3], location="Някъде", date='{}'.format(DT.datetime.now()))
# 	db.session.add(example2)
# 	db.session.commit()
