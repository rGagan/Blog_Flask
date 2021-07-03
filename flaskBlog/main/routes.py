from flask import Blueprint, request, render_template
from flaskBlog.models import Post

main = Blueprint('main', __name__)


#routes for different pages/functionality on the website
@main.route("/")
@main.route("/home")
def home():
    #to get the page number from the url query
    page = request.args.get('page', 1, type=int)

    #paginate doesn't send all the queries back. It divides the posts in pages
    #order by newest
    post = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', post=post)

@main.route("/about")
def about():
    return render_template('about.html', title='About')