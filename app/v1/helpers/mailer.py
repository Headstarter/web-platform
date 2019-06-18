from flask import Flask
from flask_mail import Mail, Message
from app.router import app

app.config['MAIL_SERVER'] = 'appssmtp.abv.bg'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'admin@headstarter.eu'
app.config['MAIL_PASSWORD'] = 'EMAIL PASSWORD'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


class Mailer:
    @staticmethod
    def sendConfirmation(new_user):
        msg = Message('', sender='headstarter@headstarter.eu', recipients=[new_user_email])
        msg.body = '''
        
        '''
        mail.send(msg)
        return "Sent"


if __name__ == '__main__':
    app.run(debug=True)
