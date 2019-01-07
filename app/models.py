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
    description = db.Column(db.String (32768))
    logo = db.Column(db.String(256))

    def __repr__(self):
        return '<Company {}>'.format(self.name) 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey('Company.id'))
    company = db.relationship('Company', back_populates='employees')
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)  

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    company_id = db.Column(db.Integer, db.ForeignKey('Company.id'))
    company = db.relationship('Company', back_populates='positions')
    description = db.Column(db.String(32768))
    def __repr__(self):
        return '<Position {}>'.format(self.name)  

import hashlib

def crypto (password):
    return hashlib.sha256(bytes(password, 'utf-8')).hexdigest()

def clear ():
    User.query.filter (True).delete ()
    Company.query.filter (True).delete ()
    Sector.query.filter (True).delete ()
    Position.query.filter (True).delete ()

def init ():
    """ Sectors """
    IT_Sector = Sector (name='Information Technologies')
    db.session.add (IT_Sector)
    db.session.commit ()
    IT_Sector = Sector.query.get (1)

    """ Companies """
    TechEdu = Company (name='TechEdu++', logo='http://infocourse.techedu.bg/img/logo.png', 
                                                description='The core aim of our projects is to create online learning management system that combines best practices in organizing trainings so that it will be interesting, useful and much easier for students.', sector = IT_Sector)
    Biodit = Company (name='Biodit Global Technologies', logo='data:image/png;base64,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', 
                                                description='BIODIT is an innovative high-technology company specialized in development of state-of-the-art security solutions, based on biometric identification.', sector = IT_Sector)
    db.session.add (TechEdu)
    db.session.add (Biodit)
    db.session.commit ()
    TechEdu = Company.query.get (1)
    Biodit = Company.query.get (2)

    """ CEOs """
    AlexTsvetanov = User (username='AlexTsvetanov', company=TechEdu, email='alex@alexts.tk', password_hash=crypto('sample password'))
    JulianSofroniev = User (username='JulianSofroniev', company=Biodit, email='julian@biodit.com', password_hash=crypto('sample password'))
    db.session.add (AlexTsvetanov)
    db.session.add (JulianSofroniev)
    db.session.commit ()

    """ Positions """
    for i in range (3):
        JuniorFrontEndDeveloper = Position (name='Junior front-end developer', company=TechEdu, 
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
● In-depth knowledge of JavaScript (ECMAScript 5)<br>
● Experience with frameworks for front-end development - Angular, React, Vue.js, etc<br>
● Knowledge of template engines - Smarty, Twig, Blade, Razor, etc<br>
● Experience in processing web pages on different platforms<br>
● Working with Related Micro Services and (RESTful) APIs<br>
● Practice with Test Driven Development, using device testing technologies<br>
● Experience with code versioning ( especially Git ) <br>
<br>
Advantages : <br>
<br>
● Understanding of the work of the HTTP protocol<br>
● Experience with Vue.js<br>
● Work with Node.js or Dart<br>
● Experience with Blade Template Engine (Laravel)<br>
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
● A more than competitive salary with (long term) incentives in accordance with your experience.<br>
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
        Designer = Position (name='Web/Graphic Designer', company=Biodit, 
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
</ul><strong></strong><strong>Please, attach a PDF portfolio of your works or specify a link to an online portfolio (Behance, Dribbble, etc). Only candidates with portfolios will be considered or contacted!<br></strong><br><strong> All applications will be treated as strictly confidential.</strong><br><strong> Please, send your CV in English language only!</strong>						 
""")
        db.session.add (JuniorFrontEndDeveloper)
        db.session.add (Designer)    
        db.session.commit ()
