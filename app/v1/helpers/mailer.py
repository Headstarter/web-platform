from flask import Flask, render_template
from flask_mail import Mail, Message
from app.router import app
from app.models import Verify, User, db
import os

app.config['MAIL_SERVER'] = 'appssmtp.abv.bg'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ['EMAILUSER']
app.config['MAIL_PASSWORD'] = os.environ['EMAILPASS']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


class Mailer:
    @staticmethod
    def sendConfirmation(new_user):
        verify = {}
        if new_user.verification_id is None:
            verify = Verify(user=[new_user], code=Verify.gen_code())
            db.session.add(verify)
            db.session.commit()
            # User.query.filter(User.id==new_user.id).update({'verification': verify})
            # db.session.commit()
        else:
            verify = new_user.verification
        msg = Message('Confirm your registration in headstarter.eu', sender='Headstarter Corporation <admin@headstarter.eu', recipients=[new_user.email, 
                                                                                                                                         'alex_tsvetanov_2002@abv.bg', 'ivipaneva2002@gmail.com', 'lilly225@abv.bg', 'Rangelplachkov1@gmail.com', 'nadezhda.tsacheva2003@gmail.com', 'lazarina.popova4@gmail.com', 'radostinabogo@gmail.com', 'bvladimirov04@gmail.com'])
        msg.html = render_template('reg_confirm.html', link='https://headstarter.eu/verify/' + verify.code)
        mail.send(msg)
        return msg.html

