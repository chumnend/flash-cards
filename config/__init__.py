import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

required = ['DATABASE_URL', 'SECRET_KEY']
for r in required:
    if r not in os.environ:
        raise ValueError(f'missing environment variable: {r}')

class Config(object):
    DECKS_PER_PAGE = 16
    DECKS_PER_USER = 8
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(object):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
