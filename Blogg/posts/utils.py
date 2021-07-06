import secrets
import os
from PIL import Image
from flask import current_app

def update_pic(picture):
    #we imported secrets to get a random hex
    #it gives a random hex of 8 bytes
    random_hex = secrets.token_hex(8)
    
    #we imported os to use these commands which separates the extension of a file
    #we use underscore for var names when we dont wanna use that in our code
    _, file_ext = os.path.splitext(picture.filename)

    pic_func = random_hex + file_ext

    return pic_func