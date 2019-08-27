from app.models import db, User, Mapper, Tag, Company, Verify, CV, Position, School, Approval
_users = []
for x in _users:
	try:
		db.session.add(User(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '
', x)
_mappers = []
for x in _mappers:
	try:
		db.session.add(Mapper(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '
', x)
_tags = []
for x in _tags:
	try:
		db.session.add(Tag(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '
', x)
_companies = []
for x in _companies:
	try:
		db.session.add(Company(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '
', x)
_verifies = []
for x in _verifies:
	try:
		db.session.add(Verify(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '
', x)
_cvs = []
for x in _cvs:
	try:
		db.session.add(CV(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '
', x)
_offers = []
for x in _offers:
	try:
		db.session.add(Position(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '
', x)
_applications = []
for x in _applications:
	try:
		db.session.add(Application(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '
', x)
schools = []
for x in schools:
	try:
		db.session.add(School(*x))
		db.session.commit()
	except Exception as e:
		db.session.rollback()
		print(str(e), '
', x)
