import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    # * App config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-pass'
    # * SQL config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')  # ? sqlite example
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # * Guard config:
    PRAETORIAN_CONFIRMATION_SENDER = os.environ.get('MAIL_USERNAME')
    PRAETORIAN_CONFIRMATION_URI = os.environ.get(
        'PRAETORIAN_CONFIRMATION_URI')
    PRAETORIAN_CONFIRMATION_SUBJECT = os.environ.get(
        'PRAETORIAN_CONFIRMATION_SUBJECT')
    JWT_ACCESS_LIFESPAN = {'minutes': 50}  # ? GUARD token lifespan
    # JWT_REFRESH_LIFESPAN = {'days': 30}
    # * Mail sender config
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or False
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_PASSWORD') or None
    ADMINS = ['beyondbaikal@gmail.com']


class DevelopmentConfig(Config):
    DEBUG = True
    SEND_FILE_MAX_AGE_DEFAULT = 0  # ? disable static file cache JS CSS
    JSON_SORT_KEYS = False
