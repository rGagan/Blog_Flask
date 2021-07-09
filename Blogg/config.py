import os

class Config:
    #setting a hash key and sqlite server 
    SECRET_KEY= os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI=os.environ.get('MYSQL_WITHCONNECTOR')
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME = os.environ.get('SERVER_EMAIL')
    MAIL_PASSWORD = os.environ.get('SERVER_EMAIL_PASS')

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True