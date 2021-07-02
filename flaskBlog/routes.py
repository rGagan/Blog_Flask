import secrets
import os
from PIL import Image
from flask import render_template, url_for, redirect, flash, request
from flaskBlog import app, db, bcrypt
from flaskBlog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskBlog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

post = [
    {
        'author': 'Shakespeare',
        'title': 'Blog 1',
        'page':'1000'
    },
    {
        'author': 'Einstein',
        'title': 'Blog 3',
        'page':'-1'
    }
]
#routes for different pages/functionality on the website
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', post=post)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    #check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= RegistrationForm()
    if form.validate_on_submit():
        #create a hashed pass for the user and adding the details onto the table
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_pass)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can login now.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form= LoginForm()
    if form.validate_on_submit():
        #match the given password with the hashed password saved in table
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'{form.email.data} logged in succesfully!', 'success')
            next_page = request.args.get('next')
            return redirect (next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful! Please check email and password.', 'danger')

    return render_template('login.html', title='Log In', form=form)

@app.route("/logout")
def logout():
    #using logout of Flask_login
    logout_user()
    return redirect(url_for('home'))


def update_pic(picture):
    #we imported secrets to get a random hex
    #it gives a random hex of 8 bytes
    random_hex = secrets.token_hex(8)
    
    #we imported os to use these commands which separates the extension of a file
    #we use underscore for var names when we dont wanna use that in our code
    _, file_ext = os.path.splitext(picture.filename)

    pic_func = random_hex + file_ext

    #we save the user's pic which they uploaded in our package
    pic_path = os.path.join(app.root_path, 'static/pfp', pic_func)

    #we installed Pillow(inside of it is PIL) to resize our file to a smaller 125px size
    new_image_size = (125, 125)
    img = Image.open(picture)
    img.thumbnail(new_image_size)

    img.save(pic_path)

    return pic_func


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    profile_img = url_for('static', filename='pfp/'+ current_user.profile_img)
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.pic.data:
            pic_newname = update_pic(form.pic.data)
            current_user.profile_img = pic_newname
        #we cange the details of current user
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your info has been updated!', 'success')

        # this is to make sure we dont submit the form when the page reloads. It sends a 'GET' request
        return redirect (url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    #checking
    return render_template('account.html', title='Account', profile_img=profile_img, form=form)