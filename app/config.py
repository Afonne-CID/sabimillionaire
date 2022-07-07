"""Flask configuration variables."""
import os
import hashlib
from os import environ, path
from decouple import config
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Set Flask configuration from .env file."""  
    # General Config
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')
    UPLOAD_FOLDER = environ.get('UPLOAD_FOLDER')
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS')
    MAIL_USE_SSL = environ.get('MAIL_USE_SSL')

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECURITY_LOGIN_URL = environ.get('SECURITY_LOGIN_URL')
    SECURITY_LOGOUT_URL = environ.get('SECURITY_LOGOUT_URL')
    ADMIN_USERNAME = environ.get('ADMIN_USERNAME')
    ADMIN_PWD = environ.get('ADMIN_PWD')

    SECURITY_PASSWORD_SALT = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    SECURITY_PASSWORD_HASH = environ.get('SECURITY_PASSWORD_HASH')
    SECURITY_POST_LOGIN_VIEW = environ.get('SECURITY_POST_LOGIN_VIEW')
    # SECURITY_LOGIN_USER_TEMPLATE = environ.get('SECURITY_LOGIN_USER_TEMPLATE')


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

class DebugConfig(Config):
    DEBUG = True

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}