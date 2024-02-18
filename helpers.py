import os
from gamelib import app

def recover_image(id):
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'cover{id}' in file_name:
            return file_name
    return 'default-cover.jpg'

def delete_file(id):
    file = recover_image(id)
    if file != 'default-cover.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file))
