from Blogg.users.utils import send_reset_email, update_pic
from Blogg import  db, bcrypt
from Blogg.models import Post, User
from Blogg.users.forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm, UpdateAccountForm
from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import current_user, login_user, login_required, logout_user
from Blogg.aws_functions import upload_img, show_img

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    #check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    form= RegistrationForm()
    if form.validate_on_submit():
        #create a hashed pass for the user and adding the details onto the table
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can login now.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    form= LoginForm()
    if form.validate_on_submit():
        #match the given password with the hashed password saved in table
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'{form.email.data} logged in succesfully!', 'success')
            next_page = request.args.get('next')
            return redirect (next_page) if next_page else redirect(url_for('home.homepage'))
        else:
            flash('Login Unsuccessful! Please check email and password.', 'danger')

    return render_template('login.html', title='Log In', form=form)

@users.route("/logout")
def logout():
    #using logout of Flask_login
    logout_user()
    return redirect(url_for('home.homepage'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    profile_img =show_img()+current_user.profile_img
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.pic.data:
            pic_newname = update_pic(form.pic.data)
            current_user.profile_img = pic_newname
            upload_img(pic_newname, form.pic.data)
        #we cange the details of current user
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your info has been updated!', 'success')

        # this is to make sure we dont submit the form when the page reloads. It sends a 'GET' request
        return redirect (url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    #checking
    return render_template('account.html', title='Account', profile_img=profile_img, form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    #to get the page number from the url query
    page = request.args.get('page', 1, type=int)

    user = User.query.filter_by(username=username).first_or_404()
    #paginate doesn't send all the queries back. It divides the posts in pages
    #order by newest
    # \ to break up to other line 
    post = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', post=post, user=user, image=show_img())

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    #check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been send to reset your password', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='Reset Password', form=form)



@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    #check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('Token is invalid or expired', 'warning')
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #create a hashed pass for the user and adding the details onto the table
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hash_pass
        db.session.commit()
        flash(f'Password for {user.username} has been updated! You can login now.', 'success')
        return redirect(url_for('users.login'))

    return render_template('reset_token.html', title='Reset Password', form=form)
