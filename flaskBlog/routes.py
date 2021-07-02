import secrets
import os
from PIL import Image
from flask import render_template, url_for, redirect, flash, request, abort
from flaskBlog import app, db, bcrypt, mail
from flaskBlog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
    PostForm, RequestResetForm, ResetPasswordForm)
from flaskBlog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

#routes for different pages/functionality on the website
@app.route("/")
@app.route("/home")
def home():
    #to get the page number from the url query
    page = request.args.get('page', 1, type=int)

    #paginate doesn't send all the queries back. It divides the posts in pages
    #order by newest
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
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


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', legend='New Post', form=form)

@app.route("/post/<int:post_id>")
def post (post_id):
    #if the post doesnt exist then show a 404 error
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', legend='Update Post', form=form)

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/user/<string:username>")
def user_posts(username):
    #to get the page number from the url query
    page = request.args.get('page', 1, type=int)

    user = User.query.filter_by(username=username).first_or_404()
    #paginate doesn't send all the queries back. It divides the posts in pages
    #order by newest
    # \ to break up to other line 
    post = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', post=post, user=user)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Link', sender='noreply@demo.com', recipients=[user.email])

    msg.body = f'''To reset your password, click on the following link:
{url_for('reset_token', token=token, _external=True)}
    
    
    
If you did not make this request, then please ignore.'''

    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    #check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been send to reset your password', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', title='Reset Password', form=form)



@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    #check if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('Token is invalid or expired', 'warning')
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #create a hashed pass for the user and adding the details onto the table
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hash_pass
        db.session.commit()
        flash(f'Password for {user.username} has been updated! You can login now.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_token.html', title='Reset Password', form=form)
