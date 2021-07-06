import secrets
import os
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from Blogg import mail

def update_pic(picture):
    #we imported secrets to get a random hex
    #it gives a random hex of 8 bytes
    random_hex = secrets.token_hex(8)
    
    #we imported os to use these commands which separates the extension of a file
    #we use underscore for var names when we dont wanna use that in our code
    _, file_ext = os.path.splitext(picture.filename)

    pic_func = random_hex + file_ext

    return pic_func
    
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Link', sender='noreply@demo.com', recipients=[user.email])

    msg.body = f'''To reset your password, click on the following link:
{url_for('users.reset_token', token=token, _external=True)}
    
    
    
If you did not make this request, then please ignore.'''

    mail.send(msg)
