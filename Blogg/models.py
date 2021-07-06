from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from Blogg import db, login_mngr
from flask_login import UserMixin

@login_mngr.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_img = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    # making s a serializer instance with the given key and expiration time. 
    def get_reset_token(self, expires_sec=900):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)

        #serializer makes a time stamp each time so s.dumps is dynamic(differenct each time)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # when we don't use self, we have to add staticmethod
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            #s.loads returns the dictionary back in the form it was dumped
            user_id=s.loads(token)['user_id']
        except:
            return None
        
        return User.query.get(user_id)

    #how should User be represented for eg in shell
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_img}')"


class Post(db.Model):

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_picture = db.Column(db.String(20), nullable=False, default='default_post.jpeg')
    content =  db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.post_picture}')"
