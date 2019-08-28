from flask import Flask, render_template
from flask_mail import Mail, Message
from app.router import app, request
from app.models import Verify, User, db
import os

if os.environ['DEBUG'] == 'off':
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
    def get_country(ip_address):
        try:
            import requests
            response = requests.get("http://api.ipstack.com/{}?access_key={}&output=json&format=1".format(ip_address, '8b255e653c775f348ffe59da14b04371'))
            js = response.json()
            import sys
            print('\n\n\n', js, '\n\n\n\n', file=sys.stdout, flush=True)
            if js['city'] == None:
                raise 'Unknown'
            country = "{}, {}, {}/{}".format (js['city'], js['region_name'], js['country_name'], js['continent_name'])
            return country
        except Exception as e:
            return "Unknown"
        
    @staticmethod
    def sendConfirmation(new_user):
        if os.environ['DEBUG'] == 'off' or True:
            if new_user.school is not None:
                import datetime
                verify = Mailer.get_verification(new_user).code
                msg = Message('Confirm teacher\'s registration in headstarter.eu', sender='Headstarter Corporation <' + os.environ['EMAILUSER'] + '>', recipients=[User.query.filter(User.id == new_user.school.admin).one().email, 'headstarter@headstarter.eu'])
                msg.html = render_template('reg_teacher_confirm.html', link='https://headstarter.eu/verify/' + verify, teacher = new_user, time = datetime.datetime.now().strftime("%H:%M on %d.%m.%Y"), location=Mailer.get_country(request.remote_addr))
                mail.send(msg)
                return msg.html
            else:
                verify = Mailer.get_verification(new_user)
                msg = Message('Confirm your registration in headstarter.eu', sender='Headstarter Corporation <' + os.environ['EMAILUSER'] + '>', recipients=[new_user.email, 'headstarter@headstarter.eu'])
                msg.html = render_template('reg_confirm.html', link='https://headstarter.eu/verify/' + verify.code)
                mail.send(msg)
                return msg.html
        
    @staticmethod
    def sendApproval(new_user):
        if os.environ['DEBUG'] == 'off':
            verify = Mailer.get_verification(new_user)
            msg = Message('Confirm your registration in headstarter.eu', sender='Headstarter Corporation <' + os.environ['EMAILUSER'] + '>', recipients=[new_user.email, 'headstarter@headstarter.eu'])
            msg.html = render_template('reg_confirm.html', link='https://headstarter.eu/verify/' + verify.code)
            mail.send(msg)
            return msg.html
    
    @staticmethod
    def sendResetPassword(user):
        if os.environ['DEBUG'] == 'off':
            verify = Mailer.get_verification(user)
            msg = Message('Reset your password in headstarter.eu', sender='Headstarter Corporation <' + os.environ['EMAILUSER'] + '>', recipients=[user.email, 'headstarter@headstarter.eu'])
            msg.html = render_template('reset_password.html', link='https://headstarter.eu/reset/' + verify.code)
            mail.send(msg)
            return msg.html
        

