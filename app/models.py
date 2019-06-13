import uuid
import hashlib
import datetime as DT
from app import db
import json


class Mapper(db.Model):
    __tablename__ = 'Mapper'
   
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(128))
    company_id = db.Column(
        db.Integer, db.ForeignKey('Company.id'), nullable=True)
    company = db.relationship('Company', back_populates='mapper')


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


class User(db.Model):
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


class Verify(db.Model):
    __tablename__ = 'Verify'
   

    id = db.Column(db.Integer, primary_key=True)

    user = db.relationship("User", back_populates="verification")
    code = db.Column(db.String(6))


class CV(db.Model):
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
    position_id = db.Column(db.Integer, db.ForeignKey(
        'Position.id'), primary_key=True)
    position = db.relationship('Position', back_populates='applications')
    company_id = db.Column(db.Integer, primary_key=True)


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
        db.session.add(User(name=name, cv=None, company=company,
                            email=email, password_hash=crypto(password)))
    db.session.commit()


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
        'tag_id': tag_id
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
        'available': True
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

    """ Companies """
    CodixBG = Company(name='Codix Bulgaria', website='https://www.codix.eu/en',
                        contacts='', logo=None,
                        description='<blockquote class="blockquote"><p class="codix-container-title"> Software solution for Commercial Finance, Supply chain Finance, Consumer Finance & Debt collection</p></blockquote>\n          \n          CODIX is the software company, which has developed iMX – a \nunique software solution, providing businesses with an event-driven \nsystem for the management of their activities, such as Factoring, \nCommercial Finance, Supply Chain Finance (SCF), Trade and Corporate \nFinance, Debt Collection and Legal, Accounts Receivable, Consumer \nFinance, Leasing, Credit Insurance, etc. Given the achievements and \ncapabilities of iMX, it is one of the best commercial finance softwares \non the market.\n            <br><br>\n          iMX is an innovative software solution, which enables our \nclients to manage all business processes within a single technical \nstructure, which can be easily customised to meet their specific needs. \nTo see how iMX software handles commercial finance system and it\'s full \ncapabilities, check out our Line of Business pages.\n            ',
                        uid="3d2f8616-f3be-45c4-8a0c-fda9702e1ff6")
    db.session.add(CodixBG)
    db.session.commit()
    """ Mappers """
    CodixBGMapper = Mapper(company_name='Codix Bulgaria', company=CodixBG)
    db.session.add(CodixBGMapper)
    db.session.commit()
    """ CEOs """
    BilyanaDakova = User(name='Биляна Дакова', company=CodixBG, verification=None, email='hr@codix.eu', password_hash='5dfee24b630b6ab628038df378866b16b459b71d1a4e386a13605b21173ef36f')
    db.session.add(BilyanaDakova)
    db.session.commit()