from flask_wtf.file import FileAllowed, FileField
from flask_wtf.form import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title=StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    post_picture = FileField('Add a post picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')

