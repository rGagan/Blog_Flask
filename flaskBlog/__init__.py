from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskBlog.config import Config

# we created the objects without parameter,
# so the objects don't initially get bound to the application and we can use them for multiple
db=SQLAlchemy()
bcrypt=Bcrypt()
login_mngr = LoginManager()

#to direct the login_required to the login page when we tryto see account info without being loggd in
login_mngr.login_view = 'users.login'
login_mngr.login_message_category = 'info'

mail = Mail()

# now we create an example app that takes its config variables from config file
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # we bind the lib objects to the app to use them inside the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_mngr.init_app(app)
    mail.init_app(app)

    # we register the packages so they're accessible in out app
    from flaskBlog.users.routes import users
    from flaskBlog.posts.routes import posts
    from flaskBlog.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    
    return app