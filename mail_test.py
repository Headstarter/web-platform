from flask import Flask
from flask_mail import Mail, Message

app =Flask(__name__)
mail=Mail(app)

app.config['MAIL_SERVER']='appssmtp.abv.bg'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'headstarter@headstarter.eu'
app.config['MAIL_PASSWORD'] = 'EMAIL PASSWORD'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/")
def index():
   msg = Message('Hello', sender = 'headstarter@headstarter.eu', recipients = ['radostinka03@gmail.com', 'nadezhda.tsacheva2003@gmail.com', 'alex_tsvetanov_2002@abv.bg'])
   msg.body = "Hello Flask message sent from Flask-Mail"
   mail.send(msg)
   return "Sent"

if __name__ == '__main__':
   app.run(debug = True)