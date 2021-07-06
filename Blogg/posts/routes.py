from Blogg.posts.forms import PostForm
from flask import Blueprint,render_template, url_for, redirect, flash, request, abort
from Blogg import db
from flask_login import current_user, login_required
from Blogg.models import Post
from Blogg.aws_functions import upload_img, show_img
from Blogg.posts.utils import update_pic

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        if form.post_picture.data:
            post_pic = update_pic(form.post_picture.data)
            upload_img(post_pic, form.post_picture.data)
            post = Post(title=form.title.data, content=form.content.data, post_picture=post_pic, author=current_user)
        else:
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
        
        db.session.add(post)
        db.session.commit()
        flash(f'Your post has been created! ', 'success')
        return redirect(url_for('home.homepage'))
    return render_template('create_post.html', title='New Post', legend='New Post', form=form)

@posts.route("/post/<int:post_id>")
def post (post_id):
    #if the post doesnt exist then show a 404 error
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, image=show_img())

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        if form.post_picture.data:
            post_pic = update_pic(form.post_picture.data)
            upload_img(post_pic, form.post_picture.data)
            post.post_picture=post_pic
        post.title = form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', legend='Update Post', form=form, image=show_img())

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home.homepage'))

