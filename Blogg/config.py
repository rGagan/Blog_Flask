import os


class Config:
    #setting a hash key and sqlite server 
    BASE_FILE=os.path.dirname(os.path.abspath(__file__))
    SECRET_KEY= os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI=os.environ.get('MYSQL_WITHCONNECTOR')
    MAIL_SERVER='smtp.googlemail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME = os.environ.get('SERVER_EMAIL')
    MAIL_PASSWORD = os.environ.get('SERVER_EMAIL_PASS')
    AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_BUCKET_NAME=os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_BUCKET_PIC=os.environ.get('AWS_BUCKET_PIC')
    AWS_S3_FILE_OVERWRITE=False
    STATIC_ROOT=os.path.join(BASE_FILE, 'staticfiles')
    

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True