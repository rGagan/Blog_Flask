from flaskBlog.models import User
from flask_wtf.form import FlaskForm
from wtforms import (
    BooleanField,
    StringField,
    FileField,
    PasswordField,
    SubmitField)

from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user


class RegistrationForm(FlaskForm):
    #setting the credentials for sqlite server
    username = StringField('Username',
                validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('Email',
                validators=[DataRequired(), Email( message="Please enter a valid email address.")])
    password = PasswordField('Password', 
                validators=[DataRequired(), Length(min=6, max=20) ])
    confpassword = PasswordField('Confirm Password',
                validators=[DataRequired(), EqualTo('password', message='The passwords must match.')])
    #recaptcha = RecaptchaField()
    submit = SubmitField('Sign Up')

    #using named methods from FlaskForm to check the availability of the username and email in User model
    def validate_username(self, username):
        usernm = User.query.filter_by(username=username.data).first()
        if usernm:
            raise ValidationError('That username is taken. Please try a different username.')

    def validate_email(self, email):
        mail = User.query.filter_by(email=email.data).first()
        if mail:
            raise ValidationError('That email is taken. Please try a different email.')

class LoginForm(FlaskForm):
    email = StringField('Email',
            validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
            validators=[DataRequired(), Length(min=6, max=20) ])
    remember = BooleanField('Keep me Signed In')
    submit = SubmitField('Log In')

class UpdateAccountForm(FlaskForm):
    #setting the credentials for sqlite server
    username = StringField('Username', 
            validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('Email', 
            validators=[DataRequired(), Email(message="Please enter a valid email address.")])
    pic = FileField('Update Profile Pic', 
            validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    #using named methods from FlaskForm to check the availability of the username and email in User model
    def validate_username(self, username):
        if username.data!=current_user.username:
            usernm = User.query.filter_by(username=username.data).first()
            if usernm:
                raise ValidationError('That username is taken. Please try a different username.')

    def validate_email(self, email):
        if email.data!=current_user.email:
            mail = User.query.filter_by(email=email.data).first()
            if mail:
                raise ValidationError('That email is taken. Please try a different email.')

class RequestResetForm(FlaskForm):
    email = StringField('Email', 
            validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        mail = User.query.filter_by(email=email.data).first()
        if mail is None:
            raise ValidationError('No such email found. Please check the email')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', 
            validators=[DataRequired(), Length(min=6, max=20) ])
    confpassword = PasswordField('Confirm Password', 
            validators=[DataRequired(), EqualTo('password', message='The passwords must match.')])
    submit = SubmitField('Reset Password')