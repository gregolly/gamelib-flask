import os

SECRET_KEY = 'your secret key'

SQLALCHEMY_DATABASE_URI = \
'{SGBD}://{user}:{password}@{server}/{database}'.format(
    SGBD = 'mysql+mysqlconnector',
    user = 'root',
    password = 'admin',
    server = 'localhost',
    database = 'gamelib'
)

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'