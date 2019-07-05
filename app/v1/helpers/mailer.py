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
    def get_verification (user):
        verify = {}
        if user.verification_id is None:
            verify = Verify(user=[user], code=Verify.gen_code())
            db.session.add(verify)
            db.session.commit()
        else:
            verify = user.verification
        return verify
        
    @staticmethod
    def sendConfirmation(new_user):
        verify = get_verification(new_user)
        msg = Message('Confirm your registration in headstarter.eu', sender='Headstarter Corporation <' + os.environ['EMAILUSER'] + '>', recipients=[new_user.email, 'headstarter@headstarter.eu'])
        msg.html = render_template('reg_confirm.html', link='https://headstarter.eu/verify/' + verify.code)
        mail.send(msg)
        return msg.html
    
    @staticmethod
    def sendResetPassword(user):
        verify = get_verification(user)
        msg = Message('Reset your password in headstarter.eu', sender='Headstarter Corporation <' + os.environ['EMAILUSER'] + '>', recipients=[user.email, 'headstarter@headstarter.eu'])
        msg.html = render_template('reset_password.html', link='https://headstarter.eu/reset/' + verify.code)
        mail.send(msg)
        return msg.html
        

