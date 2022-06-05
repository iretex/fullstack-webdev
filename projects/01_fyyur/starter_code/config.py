import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
dialect = 'postgresql'
username = 'postgres'
password = 'iretex'
host = '127.0.0.1'
port = 5432
database = 'fyyur'
SQLALCHEMY_DATABASE_URI = f'{dialect}://{username}:{password}@{host}:{port}/{database}' #'<Put your local database url>'
SQLALCHEMY_TRACK_MODIFICATIONS = False
