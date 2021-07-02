import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

#setting a hash key and sqlite server 
app.config['SECRET_KEY']= 'bd2678a1ea518bdb3c288d70c39ffed2'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

#creating variables for flask libraries
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_mngr = LoginManager(app)

#to direct the login_required to the login page when we tryto see account info without being loggd in
login_mngr.login_view = 'login'
login_mngr.login_message_category = 'info'


app.config['MAIL_SERVER']='smtp.googlemail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME'] = os.environ.get('SERVER_EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('SERVER_EMAIL_PASS')
mail = Mail(app)


from flaskBlog import routes