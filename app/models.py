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


class Position(db.Model):
    __tablename__ = 'Position'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    company_id = db.Column(db.Integer, db.ForeignKey('Company.id'))
    company = db.relationship('Company', back_populates='positions')
    description = db.Column(db.String(32768))
    available = db.Column(db.Boolean)
    duration = db.Column(db.Integer)
    hours_per_day = db.Column(db.String(128))
    age_required = db.Column(db.String(128))
    tag_id = db.Column(db.Integer, db.ForeignKey('Tag.id'))
    tag = db.relationship('Tag', back_populates='positions')
    applications = db.relationship("Application", back_populates="position")


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


def insert_position(name, company_id, description, available, duration, hours_per_day, age_required, tag_id):
    p = Position(
        name=name,
        company_id=company_id,
        description=description,
        available=available,
        duration=duration,
        hours_per_day=hours_per_day,
        age_required=age_required,
        tag_id=tag_id
    )
    db.session.add(p)
    db.session.commit()
    return p.id


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
    Headstarter = Company(name='Headstarter', website='https://headstarter.eu',
                          contacts='Mail Us: contact@headstarter.eu', logo='/static/img/company/1.png',
                          description='We are connecting students and business.', uid=gen_uid())
    db.session.add(Headstarter)
    db.session.commit()

    Biodit = Company(name='Biodit Global Technologies', website='https://biodit.com',
                     contacts="""
                     Visit Us: бул. „св. Климент Охридски“ 125, 1756 кв. Малинова долина, София<br>
                     Mail Us: pr@biodit.com, office@biodit.com""", logo='/static/img/company/2.png',
                     description='Example of description', uid=gen_uid())
    db.session.add(Biodit)
    db.session.commit()

    Deamix = Company(name='Dreamix', website='',
                     contacts="", logo='/static/img/company/3.png',
                     description='', uid=gen_uid())

    BICA_services = Company(name='BICA services', website='',
                     contacts="", logo='/static/img/company/4.png',
                     description='', uid=gen_uid())

    iGreet = Company(name='iGreet', website='',
                     contacts="", logo='/static/img/company/5.png',
                     description='', uid=gen_uid())

    db.session.add(Deamix)
    db.session.add(BICA_services)
    db.session.add(iGreet)
    db.session.commit()

    """ CEOs """
    insert_user(name='Alex Tsvetanov', company=Headstarter, email='alex@alexts.tk', password=crypto('password'))

    """ Positions """
    example1 = Position(name='Python Web Developer', company=Headstarter,
                       description="<strong>Пробно</strong> <i>описание</i> на <u>стажанстка програма</u>",
                       available=True, duration=3, hours_per_day="7-8ч.",
                       age_required='Поне 16 г.', tag=Tags_db[3])
    db.session.add(example1)
    db.session.commit()

    example2 = Position(name='C/C++ Back-end Developer', company=Headstarter,
                       description="""
Takeaway.com is Europe’s leading online and mobile food ordering company, dedicated to connecting consumers with their favorite local restaurants. The people who work at Takeaway.com are our company's greatest asset; each person at Takeaway.com plays an integral part in building tools and technology that help connect and transact our consumers and restaurants - at scale.<br>
<br>
The company’s online and mobile ordering platforms allow meals to order directly from more than 40,000 takeout restaurants all over Europe and beyond. The Takeaway.com portfolio of brands includes Takeaway.com, Thuisbezorgd.nl, Lieferando.de, Pyszne.pl, Lieferservice.at and Vietnammm.com. The working atmosphere at Takeaway.com is characterized by team spirit, trust and open communication as well as a high degree of personal responsibility. Bringing in your own ideas is encouraged and creativity, motivation and commitment are much appreciated.<br>
<br>
The Position: <br>
<br>
We are looking for talented Front-End Developers to join our multinational and multicultural IT organization. You will play a key role in helping on our journey towards high performance teams following agile values and principles.<br>
<br>
Your Profile: <br>
<br>
● At least 3 years of professional experience<br>
● Excellent knowledge of HTML 5, CSS 3 and DOM<br>
● In-depth knowledge of JavaScript(ECMAScript 5)<br>
● Experience with frameworks for front-end development - Angular, React, Vue.js, etc<br>
● Knowledge of template engines - Smarty, Twig, Blade, Razor, etc<br>
● Experience in processing web pages on different platforms<br>
● Working with Related Micro Services and(RESTful) APIs<br>
● Practice with Test Driven Development, using device testing technologies<br>
● Experience with code versioning( especially Git ) <br>
<br>
Advantages : <br>
<br>
● Understanding of the work of the HTTP protocol<br>
● Experience with Vue.js<br>
● Work with Node.js or Dart<br>
● Experience with Blade Template Engine(Laravel)<br>
● Familiarity or experience with ECMAScript 6 in JavaScript<br>
● Familiarity or experience with TypeScript<br>
● Task trainer experience - Grunt, Gulp, etc.<br>
● Familiarity or experience with Webpack and / or Laravel-mix<br>
● Knowledge of CSS preprocessors -LESS, SASS<br>
● Experience with Bootstrap framework<br>
● Experience with Test Driven Development, using device testing technologies<br>
● Experience or familiarity with the Scrum methodology<br>
<br>
What We offer? <br>
<br>
● A place where your ideas are heard and where you can really grow and learn with your team.<br>
● A more than competitive salary with(long term) incentives in accordance with your experience.<br>
● Awesome teams and people, in a fast growing company.<br>
● Being part of a young, professional and truly international team.<br>
● The opportunity to learn new concepts and practice them in a safe environment.<br>
● The freedom to go where no one in our company has gone before.<br>
● Free drinks, fruit, several sports benefits and regular awesome team events<br>
<br>
Takeaway offers career advancement and lucrative compensation. The Technology department has regular knowledge sharing, training and attends/speaks at global conferences<br>
<br>
How to apply?<br>
<br>
If you are interested, follow the link below and please send us your CV / Resume.<br>
We will read all the information on it and we will contact the most suitable candidates.<br>
Your personal data is protected by Bulgarian law and European General Data Protection Regulation.<br>
""",
                       available=True, duration=6, hours_per_day="До 4ч.",
                       age_required='Поне 16 г.', tag=Tags_db[3])
    db.session.add(example2)
    db.session.commit()

    # Students
    insert_user(name='Nadegda Tsacheva', company=None, email='nadeto@headstarter.eu', password=crypto('password'))
