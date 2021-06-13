# -*- coding: utf-8 -*-
from app.models import db, User, Mapper, Tag, Company, Verify, CV, Position, School, Approval, Application
print('Users:')
_users = []
for x in _users:
	try:
		db.session.add(User(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '\n', x)
print("Done")
print("Mappers:")
_mappers = []
for x in _mappers:
	try:
		db.session.add(Mapper(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '\n', x)
print("Done")
print("Tags:")
_tags = [(1, 'Aviation'), (2, '&nbsp;&nbsp;&nbsp; Aircraft Dispatcher'), (3, '&nbsp;&nbsp;&nbsp; Aircraft Mechanic'), (4, '&nbsp;&nbsp;&nbsp; Airline Pilot'), (5, '&nbsp;&nbsp;&nbsp; Federal Air Marshal'), (6, '&nbsp;&nbsp;&nbsp; Flight Attendant'), (7, 'Arts'), (8, '&nbsp;&nbsp;&nbsp; Actor'), (9, '&nbsp;&nbsp;&nbsp; Architect'), (10, '&nbsp;&nbsp;&nbsp; Art Appraiser'), (11, '&nbsp;&nbsp;&nbsp; Artist Museum Jobs'), (12, '&nbsp;&nbsp;&nbsp; Music Conductor'), (13, '&nbsp;&nbsp;&nbsp; Designer'), (14, 'Business'), (15, '&nbsp;&nbsp;&nbsp; Accountant'), (16, '&nbsp;&nbsp;&nbsp; Administrative Assistant'), (17, '&nbsp;&nbsp;&nbsp; Advertising'), (18, '&nbsp;&nbsp;&nbsp; Financal Advisor'), (19, '&nbsp;&nbsp;&nbsp; Goverment Jobs'), (20, '&nbsp;&nbsp;&nbsp; Human Resourses'), (21, '&nbsp;&nbsp;&nbsp; Insurance Agent'), (22, '&nbsp;&nbsp;&nbsp; Investment Banker'), (23, '&nbsp;&nbsp;&nbsp; Lawyer'), (24, '&nbsp;&nbsp;&nbsp; Analyst'), (25, '&nbsp;&nbsp;&nbsp; Marketing'), (26, 'Media'), (27, '&nbsp;&nbsp;&nbsp; Publisher'), (28, '&nbsp;&nbsp;&nbsp; Public Relations'), (29, '&nbsp;&nbsp;&nbsp; Writer/Editor'), (30, '&nbsp;&nbsp;&nbsp; Journalist'), (31, '&nbsp;&nbsp;&nbsp; Copywriter'), (32, '&nbsp;&nbsp;&nbsp; Producer'), (33, 'Medical'), (34, '&nbsp;&nbsp;&nbsp; Nurse'), (35, '&nbsp;&nbsp;&nbsp; Orthodonist'), (36, '&nbsp;&nbsp;&nbsp; Paramedic'), (37, '&nbsp;&nbsp;&nbsp; Pediatrician'), (38, '&nbsp;&nbsp;&nbsp; Psychiatrist'), (39, '&nbsp;&nbsp;&nbsp; Psychologisst'), (40, '&nbsp;&nbsp;&nbsp; Social Worker'), (41, '&nbsp;&nbsp;&nbsp; Vet'), (42, 'Service Industry'), (43, '&nbsp;&nbsp;&nbsp; Bank Teller'), (44, '&nbsp;&nbsp;&nbsp; Call Canter'), (45, '&nbsp;&nbsp;&nbsp; Hair Stylist'), (46, '&nbsp;&nbsp;&nbsp; Cook'), (47, '&nbsp;&nbsp;&nbsp; Construction Worker'), (48, '&nbsp;&nbsp;&nbsp; Retail Sales'), (49, '&nbsp;&nbsp;&nbsp; Sports Instructor'), (50, '&nbsp;&nbsp;&nbsp; Waiter'), (51, '&nbsp;&nbsp;&nbsp; Event Planer'), (52, 'Teaching'), (53, '&nbsp;&nbsp;&nbsp; Career Conselor'), (54, '&nbsp;&nbsp;&nbsp; College Pfoffesor'), (55, '&nbsp;&nbsp;&nbsp; School Jobs'), (56, '&nbsp;&nbsp;&nbsp; Substituve Teacher'), (57, '&nbsp;&nbsp;&nbsp; Teacher'), (58, 'Technology'), (59, '&nbsp;&nbsp;&nbsp; App Developer'), (60, '&nbsp;&nbsp;&nbsp; Back-End Developer'), (61, '&nbsp;&nbsp;&nbsp; Computer Programer'), (62, '&nbsp;&nbsp;&nbsp; Computer Systems'), (63, '&nbsp;&nbsp;&nbsp; Database Administrator'), (64, '&nbsp;&nbsp;&nbsp; Front End'), (65, '&nbsp;&nbsp;&nbsp; Software Developer'), (66, '&nbsp;&nbsp;&nbsp; Web Developer'), (67, '&nbsp;&nbsp;&nbsp; Hardware Engineer')]
for x in _tags:
	try:
		db.session.add(Tag(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '\n', x)
print("Done")
print("Companies:")
_companies = []
for x in _companies:
	try:
		db.session.add(Company(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '\n', x)
print("Done")
print("Verifies:")
_verifies = []
for x in _verifies:
	try:
		db.session.add(Verify(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '\n', x)
print("Done")
print("CVs:")
_cvs = []
for x in _cvs:
	try:
		db.session.add(CV(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '\n', x)
print("Done")
print("Positions:")
_offers = []
for x in _offers:
	try:
		db.session.add(Position(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '\n', x)
print("Done")
print("Applications:")
_applications = []
for x in _applications:
	try:
		db.session.add(Application(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '\n', x)
print("Done")
print("Schools:")
schools = []
for x in schools:
	try:
		db.session.add(School(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '\n', x)
