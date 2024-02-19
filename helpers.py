import os
from gamelib import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField

class GameForm(FlaskForm):
    name = StringField('Game name', [validators.data_required(), validators.length(min=1, max=50)])
    category = StringField('Category', [validators.data_required(), validators.length(min=1, max=40)])
    console = StringField('Console', [validators.data_required(), validators.length(min=1, max=20)])
    save = SubmitField('Save')
    

def recover_image(id):
    for file_name in os.listdir(app.config['UPLOAD_PATH']):
        if f'cover{id}' in file_name:
            return file_name
    return 'default-cover.jpg'

def delete_file(id):
    file = recover_image(id)
    if file != 'default-cover.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file))


