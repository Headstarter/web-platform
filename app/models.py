from app import db


class Sector(db.Model):
    __tablename__ = 'Sector'
    id = db.Column(db.Integer, primary_key=True)
    companies = db.relationship("Company", back_populates="sector")

    name = db.Column(db.String(128))

    def __repr__(self):
        return '<Sector {}>'.format(self.name)  


class Company(db.Model):
    __tablename__ = 'Company'
    id = db.Column(db.Integer, primary_key=True)
    sector_id = db.Column(db.Integer, db.ForeignKey('Sector.id'))
    sector = db.relationship("Sector", back_populates="companies")

    employees = db.relationship("User", back_populates="company")
    positions = db.relationship("Position", back_populates="company")

    name = db.Column(db.String(128), unique=True)
    description = db.Column(db.String(32768))
    logo = db.Column(db.String(256))
    website = db.Column(db.String(256))
    contacts = db.Column(db.String(32768))

    email = db.Column(db.String(1024))
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<Company {}>'.format(self.name) 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey('Company.id'), nullable=True)
    company = db.relationship('Company', back_populates='employees')
    password_hash = db.Column(db.String(128))
    type_registration = db.Column(db.String(64))


    def to_dict(self):
        return {"id": self.id,
                "name": self.username,
                "email": self.email,
                "company": self.company,
               }

    def __repr__(self):
        return '<User {}>'.format(self.username)  


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    company_id = db.Column(db.Integer, db.ForeignKey('Company.id'))
    company = db.relationship('Company', back_populates='positions')
    description = db.Column(db.String(32768))
    available = db.Column(db.Boolean)
    time = db.Column(db.String(12))
    place = db.Column(db.String())

    def __repr__(self):
        return '<Position {}>'.format(self.name)  


import hashlib


def crypto(password):
    return hashlib.sha256(bytes(password, 'utf-8')).hexdigest()


def clear():
    User.query.filter(True).delete()
    Company.query.filter(True).delete()
    Sector.query.filter(True).delete()
    Position.query.filter(True).delete()


def insert_user(name, email, password, _type, company=None):
    db.session.add(User(username=name, company=company, email=email, password_hash=crypto(password), type_registration=_type))
    db.session.commit()


def insert_company(sector_id, name, description, logo, website, contacts):
    sector = Sector.query.filter(Sector.id == sector_id).one()
    db.session.add(Company(
        sector_id=sector, sector=sector,
        name=name, description=description,
        logo=logo, website=website, contacts=contacts))
    db.session.commit()


def init():
    """ Sectors """
    IT_Sector = Sector(name='Information Technologies')
    db.session.add(IT_Sector)
    db.session.commit()
    IT_Sector = Sector.query.get(1)

    """ Companies """
    TechEdu = Company(password=crypto('sample password'), email='headstarter@techedu.bg', name='TechEdu++', website='http://techedu.bg', contacts='Mail Us: contact@techedu.bg', logo='http://infocourse.techedu.bg/img/logo.png',
                                                description='The core aim of our projects is to create online learning management system that combines best practices in organizing trainings so that it will be interesting, useful and much easier for students.', sector = IT_Sector)
    Biodit = Company(password=crypto('sample password'), email='headstarter@biodit.com', name='Biodit Global Technologies', website='https://biodit.com', contacts='Visit Us: бул. „св. Климент Охридски“ 125, 1756 кв. Малинова долина, София<br>Mail Us: pr@biodit.com, office@biodit.com', logo='/static/img/biodit.png',
                                                description='BIODIT is an innovative high-technology company specialized in development of state-of-the-art security solutions, based on biometric identification.', sector = IT_Sector)
    db.session.add(TechEdu)
    db.session.add(Biodit)
    db.session.commit()
    TechEdu = Company.query.get(1)
    Biodit = Company.query.get(2)

    """ CEOs """
    AlexTsvetanov = User(username='Alex Tsvetanov', company=TechEdu, email='alex@alexts.tk', password_hash=crypto('sample password'), type_registration='fb')
    JulianSofroniev = User(username='Julian Sofroniev', company=Biodit, email='julian@biodit.com', password_hash=crypto('sample password'), type_registration='standard')
    db.session.add(AlexTsvetanov)
    db.session.add(JulianSofroniev)
    db.session.commit()
    AlexTsvetanov = User.query.get(1)
    JulianSofroniev = User.query.get(2)

    """ Positions """
    for i in range(3):
        JuniorFrontEndDeveloper = Position(place="Remote", time="Full-time", available=True, name='Junior front-end developer', company=TechEdu,
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
""")
        Designer = Position(time="Part-time", place="Remote", available=True, name='Web/Graphic Designer', company=Biodit,
description="""
<strong>This is why we need you</strong><br><br>We’re proud of the journey across all digital platforms so far, but a major focus for us in 2018 is evolving our brand to the next level and this is where you come in, developing creative ideas and concepts, as well as meeting tight deadlines.<br>We are looking for a full-time Graphic/Web Designer to join Reward Gateway with strong Adobe Creative Suite skills to bring magic to all our clients’ brand by creating high-quality visuals.<br><br><strong>On this position you will be responsible for:</strong><br><ul><li>Communicating with account managers to discuss the client/business objectives and requirements of the job</li>
<li>Interpreting the client’s business needs and producing web/print visuals in accordance with design briefs and brand guidelines</li>
<li>Producing visuals with high impact - both in print and web media&nbsp;</li>
<li>Online design including&nbsp;Web page layouts build through our SmartHub® product Other web and social network visuals</li>
</ul><strong>Technical knowledge and skills:</strong><br><ul><li>Proficiency in Adobe Creative Suite – good skills in Photoshop, Illustrator and InDesign. Proficiency in InDesign is a big plus!&nbsp;</li>
<li>Fluent in spoken and written English</li>
<li>Experience in creating web graphics</li>
<li>Excellent attention to detail and proven ability to meet deadlines</li>
<li>Able to act on own initiative, delivering projects without immediate supervision</li>
<li>A 'can do' approach, willingness to learn</li>
<li>Ability to work well under pressure</li>
<li>An enthusiastic team player</li>
<li>Good working knowledge of Mac is desirable, but not compulsory</li>
</ul><br><strong>This is what we do</strong><br><br>We create products for HR. Products that are innovative, easy to use and deliver high engagement for every one of our clients. High engagement is what makes our clients happy and that client number is growing fast. We currently work with over 1700 companies including American Express, Groupon, Yahoo!, IBM, and McDonald’s. Each client uses our core product SmartHub, an employee engagement platform which allows them to build an employee experience unique to their organisation.<br><br>We strictly “solve for HR,” if you ever join us you’ll hear us say that a lot. HR is our customer, we understand their world and their world only, we care passionately about what they achieve in their role, and we’re here to help them. Our mission is to make the world a better place to work.<br><br><strong>This is how we take care of you<br></strong>
<ul><li>35 days holiday including public holidays</li>
<li>Employee Share Ownership</li>
<li>Family Leave</li>
<li>Parental Leave</li>
<li>Wellbeing Choice - Annual allowance to spend on your wellbeing</li>
<li>Life Insurance</li>
<li>Bonus if you suggest someone who we hire</li>
<li>Bonus if you get married or have a civil partnership</li>
<li>Bonus if you have or adopt a child</li>
<li>6 month unpaid sabbatical after 5 years</li>
<li>Salary Advance</li>
<li>Volunteer Days</li>
<li>Book benefit</li>
<li>Bring your dog to work</li>
<li>Free breakfast items and soft drinks</li>
<li>Food vouchers</li>
<li>Private Medical Insurance</li>
</ul><strong></strong><strong>Please, attach a PDF portfolio of your works or specify a link to an online portfolio(Behance, Dribbble, etc). Only candidates with portfolios will be considered or contacted!<br></strong><br><strong> All applications will be treated as strictly confidential.</strong><br><strong> Please, send your CV in English language only!</strong>						 
""")
        db.session.add(JuniorFrontEndDeveloper)
        db.session.add(Designer)    
        db.session.commit()

    # Students

    NadegdaTsacheva = User(username='Nadegda Tsacheva', company=None, email='nadegda@headstarter.eu', password_hash=crypto('sample password'), type_registration='standard')
    db.session.add(NadegdaTsacheva)
    db.session.commit()
    NadegdaTsacheva = User.query.get(3)
