import uuid
import hashlib
import datetime as DT
from app import db
import json

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Mapper(Base, db.Model):
    __tablename__ = 'Mapper'
   
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(128))
    company_id = db.Column(
        db.Integer, db.ForeignKey('Company.id'), nullable=True)
    company = db.relationship('Company', back_populates='mapper')


class Tag(Base, db.Model):
    __tablename__ = 'Tag'
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    positions = db.relationship("Position", back_populates="tag")

    def __repr__(self):
        return '<Tag ' + str(self.id) + ' - ' + str(self.name) + '>'


class Company(Base, db.Model):
    __tablename__ = 'Company'
   
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(256))

    mapper = db.relationship("Mapper", back_populates="company")
    employees = db.relationship("User", back_populates="company")
    positions = db.relationship("Position", back_populates="company")

    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(32768))
    logo = db.Column(db.String(256))
    website = db.Column(db.String(256))
    contacts = db.Column(db.String(32768))

    def __repr__(self):
        return '<Company {}, {}, {}>'.format(self.id, self.uid, self.name)


class User(Base, db.Model):
    __tablename__ = 'User'
   

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    cv_id = db.Column(db.Integer, db.ForeignKey('CV.id'), nullable=True)
    cv = db.relationship('CV', back_populates='user', uselist=False)

    verification_id = db.Column(
        db.Integer, db.ForeignKey('Verify.id'), nullable=True)
    verification = db.relationship(
        'Verify', back_populates='user', uselist=False)

    company_id = db.Column(
        db.Integer, db.ForeignKey('Company.id'), nullable=True)
    company = db.relationship('Company', back_populates='employees')

    applications = db.relationship("Application", back_populates="user")

    def to_dict(self):
        return {"id": self.id,
                "name": self.name,
                "email": self.email,
                "company": self.company
                }

    def is_verified():
        return verification_id is None

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Verify(Base, db.Model):
    __tablename__ = 'Verify'
   

    id = db.Column(db.Integer, primary_key=True)

    user = db.relationship("User", back_populates="verification")
    code = db.Column(db.String(6))
    
    
    @staticmethod
    def gen_code():
        import random
        alphabet = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
        return ''.join(random.choice(alphabet) for i in range(16)) # 10 ^ 28.678267031972062 variants


class CV(Base, db.Model):
    __tablename__ = 'CV'

    id = db.Column(db.Integer, primary_key=True)

    user = db.relationship("User", back_populates="cv")

    photo = db.Column(db.String(256))
    name = db.Column(db.String(256))
    email = db.Column(db.String(256))
    telephone = db.Column(db.String(16))
    birthday = db.Column(db.String(256))
    location = db.Column(db.String(256))
    about = db.Column(db.String(512))
    # achievements

    education = db.Column(db.String(2048))
    projects = db.Column(db.String(2048))
    skills = db.Column(db.String(512))
    languages = db.Column(db.String(512))
    hobbies = db.Column(db.String(512))

    def get_skills(self):
        self.skills = self.skills or '[]'
        return json.loads(self.skills)

    def get_projects(self):
        self.projects = self.projects or '[]'
        return json.loads(self.projects)

    def get_education(self):
        self.education = self.education or '[]'
        return json.loads(self.education)

    def get_languages(self):
        self.languages = self.languages or '[]'
        return json.loads(self.languages)

    def get_hobbies(self):
        self.hobbies = self.hobbies or '[]'
        return json.loads(self.hobbies)

    def __repr__(self):
        return '<CV {}>'.format(self.name)


class Position(Base, db.Model):
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
        elif today - DT.timedelta(hours=24) < posted:
            return "{} hours ago".format(int((today - posted).total_seconds() / 60.0 / 60.0))
        elif today - DT.timedelta(days=7) < posted:
            return "{} days ago".format(int((today - posted).total_seconds() / 60.0 / 60.0 / 24.0))
        if today - DT.timedelta(weeks=2) > posted:
            return "{} weeks ago".format(int((today - posted).total_seconds() / 7.0 / 60.0 / 60.0 / 24.0))
        if today - DT.timedelta(weeks=1) > posted:
            return "{} week ago".format(int((today - posted).total_seconds() / 7.0 / 60.0 / 60.0 / 24.0))


class Application (Base, db.Model):
    __tablename__ = 'Application'
   
    id = db.Column(db.String(2048), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    user = db.relationship('User', back_populates='applications')
    position_id = db.Column(db.Integer, db.ForeignKey(
        'Position.id'), primary_key=True)
    position = db.relationship('Position', back_populates='applications')
    company_id = db.Column(db.Integer, primary_key=True)


def factory(classname):
    cls = globals()[classname]
    return cls


def gen_uid():
    return str(uuid.uuid4())


def crypto(password):
    return hashlib.sha256(bytes(password, 'utf-8')).hexdigest()


def clear():
    User.query.filter(True).delete()
    Company.query.filter(True).delete()
    Tag.query.filter(True).delete()
    Position.query.filter(True).delete()
    Mapper.query.filter(True).delete()
    CV.query.filter(True).delete()
    Application.query.filter(True).delete()
    Verify.query.filter(True).delete()


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


def insert_user(name, email, password, company=None ,director=None):
    new_user = {}
    if company is None:
        if director is None:
            new_user = User(name=name, cv=CV(photo='/static/img/cv/' + str(email) + '.jpg',
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
                                             hobbies='[]',
                                             school=' '
                                             ), company=company, email=email, password_hash=crypto(password))
        else:
            new_user = User(name=name, 
                            school=school, 
                            cv=None, 
                            email=email, 
                            password_hash=crypto(password))
    else:
        new_user = User(name=name, cv=None, company=company,
                            email=email, password_hash=crypto(password))
    db.session.add(new_user)
    db.session.commit()
    
    from app.v1.helpers.mailer import Mailer
    Mailer.sendConfirmation(new_user)


def insert_application(user_id, position_id):
    try:
        company_id = Position.query.filter(
            Position.id == position_id).one().company_id
        db.session.add(Application(id=str(user_id)+'_'+str(position_id),
                                   user_id=user_id, position_id=position_id, company_id=company_id))
        db.session.commit()
    except:
        return False


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
        'tag_id': tag_id,
        'available': available
    })
    db.session.commit()
    return position_id


def insert_company(name):
    uid = gen_uid()
    company = Company(
        uid=uid,
        name=name,
        website='',
        description='',
        logo='/images/company/' + str(uid) + '.png'
    )
    
    import os
    import shutil
    shutil.copy(os.path.join(os.environ['basedir'], 'static/wt_prod-20039/images/company/150.png'),os.path.join(os.environ['basedir'], 'static/wt_prod-20039/images/company/' + str(uid) + '.png'))
    
    db.session.add(company)
    db.session.commit()
    db.session.add(Mapper(company_name=name, company_id=Company.query.filter(
        Company.name == name).one().id))
    db.session.commit()
    import sys
    print('returned Company', Company.query.filter(
        Company.name == name).one())
    return Company.query.filter(Company.name == name).one()


def update_company(company_id, name, website, description):
    Company.query.filter(Company.id == company_id).update({
        'name': name,
        'website': website,
        'description': description
    })
    db.session.commit()
    return company_id


def update_cv(student_id, name, email, telephone, location,
              birthday, languages, education, projects, description, skills, hobbies):
    import sys
    print(student_id, name, email, telephone, location,
          birthday, languages, education, projects, description)
    print('All User with id', student_id, 'are', User.query.filter(
        User.id == student_id).all())
    cv_id = User.query.filter(User.id == student_id).one().cv_id
    print(cv_id)
    CV.query.filter(CV.id == cv_id).update({
        'name': name,
        'email': email,
        'telephone': telephone,
        'location': location,
        'birthday': birthday,
        'languages': languages,
        'education': education,
        'projects': projects,
        'skills': skills,
        'hobbies': hobbies,
        'about': description
    })
    db.session.commit()
    return cv_id


def activate_position(position_id):
    Position.query.filter(Position.id == position_id).update({
        'available': True
    })
    db.session.commit()
    return position_id


def deactivate_position(position_id):
    Position.query.filter(Position.id == position_id).update({
        'available': False
    })
    db.session.commit()
    return position_id


def filter_applications(position=None, company=None):
    if position is None:
        applications = Application.query
    else:
        applications = Application.query.filter(
            Application.position_id == position)
    if company is None:
        applications = applications
    else:
        applications = applications.filter(Application.company_id == company)
    return applications


def filter_offers_by_tag(position=None, company=None, group=None):
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
    elif position == None:
        positions = Position.query.filter(Position.available == True)
    else:
        positions = Position.query.filter(Position.available == True) \
            .filter(Position.tag_id == position)

    if company is not None:
        positions = positions.filter(Position.company_id == company)
        
    if group is not None:
        from app.v1.target import groups, Target_Group
        print('in', groups[int(group)]['tags'])
        from sqlalchemy import or_
        positions = positions.filter(or_(*[Position.tag_id.like(x) for x in groups[int(group)]['tags']]))
        print(positions.all())

    return positions.order_by(Position.id.desc())

def filter_all_offers_by_tag(position=None, company=None, group=None):
    if position is None:
        positions = Position.query.filter(True)

    elif position == 1:
        positions = Position.query.filter(True) \
            .filter(Position.tag_id <= 9)

    elif position == 10:
        positions = Position.query.filter(True) \
            .filter(Position.tag_id > 9) \
            .filter(Position.tag_id <= 14)

    elif position == 15:
        positions = Position.query.filter(True) \
            .filter(Position.tag_id > 14) \
            .filter(Position.tag_id <= 21)

    elif position == 22:
        positions = Position.query.filter(True) \
            .filter(Position.tag_id > 21) \
            .filter(Position.tag_id <= 28)

    elif position == 29:
        positions = Position.query.filter(True) \
            .filter(Position.tag_id > 28) \
            .filter(Position.tag_id <= 32)
    elif position == None:
        positions = Position.query.filter(True)
    else:
        positions = Position.query.filter(True) \
            .filter(Position.tag_id == position)

    if company is not None:
        positions = positions.filter(Position.company_id == company)
        
    if group is not None:
        from app.v1.target import groups, Target_Group
        print('in', groups[int(group)]['tags'])
        from sqlalchemy import or_
        positions = positions.filter(or_(*[Position.tag_id.like(x) for x in groups[int(group)]['tags']]))
        print(positions.all())

    return positions.order_by(Position.id.desc())


def init():
    """ Tag """
    tags = [
        'Software Engineer', '&nbsp;&nbsp;&nbsp; Mobile Developer', '&nbsp;&nbsp;&nbsp; Frontend Developer', '&nbsp;&nbsp;&nbsp; Backend Developer', '&nbsp;&nbsp;&nbsp; Full-Stack Developer', '&nbsp;&nbsp;&nbsp; Engineering Manager', '&nbsp;&nbsp;&nbsp; QA Engineer', '&nbsp;&nbsp;&nbsp; DevOps', '&nbsp;&nbsp;&nbsp; Software Architect', 'Designer', '&nbsp;&nbsp;&nbsp; UI/UX Designer', '&nbsp;&nbsp;&nbsp; User Researcher', '&nbsp;&nbsp;&nbsp; Visual Designer', '&nbsp;&nbsp;&nbsp; Creative Director', 'Operations', '&nbsp;&nbsp;&nbsp; Finance/Accounting', '&nbsp;&nbsp;&nbsp; H.R.', '&nbsp;&nbsp;&nbsp; Office Manager', '&nbsp;&nbsp;&nbsp; Recruiter', '&nbsp;&nbsp;&nbsp; Customer Service', '&nbsp;&nbsp;&nbsp; Operations Manager', 'Sales', '&nbsp;&nbsp;&nbsp; Business Development', '&nbsp;&nbsp;&nbsp; Sales Development', '&nbsp;&nbsp;&nbsp; Account Executive', '&nbsp;&nbsp;&nbsp; BD Manager', '&nbsp;&nbsp;&nbsp; Account Manager', '&nbsp;&nbsp;&nbsp; Sales Manager', 'Marketing', '&nbsp;&nbsp;&nbsp; Growth Hacker', '&nbsp;&nbsp;&nbsp; Marketing Manager', '&nbsp;&nbsp;&nbsp; Content Creator', 'Hardware Engineer', 'Mechanical Engineer', 'Systems Engineer', 'Business Analyst', 'Data Scientist', 'Product Manager', 'Project Manager'  # , 'Attorney', '&nbsp;&nbsp;&nbsp; CEO', '&nbsp;&nbsp;&nbsp; CFO', '&nbsp;&nbsp;&nbsp; CMO', '&nbsp;&nbsp;&nbsp; COO', '&nbsp;&nbsp;&nbsp; CTO'
    ]
    Tags_db = []
    for x in tags:
        tag = Tag(name=x)
        db.session.add(tag)
        db.session.commit()
        print(Tag.query.get(len(Tags_db) + 1), end=' ')
        Tags_db.append(Tag.query.get(len(Tags_db) + 1))
    print()