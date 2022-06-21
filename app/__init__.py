import os
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module


db = SQLAlchemy()
login_manager = LoginManager()
basedir = os.path.abspath(os.path.dirname(__file__))


def register_extensions(app):
    db.init_app(app) # Initializes the database
    login_manager.init_app(app) #Initializes login manager
    migrate = Migrate(app, db)

def register_blueprints(app):
    for module_name in ('auth', 'home', 'transaction', 'blog'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    # @app.before_first_request
    # def initialize_database():
    #     db.create_all()

    @app.teardown_request
    def shutdown_session2(exception=None):
        db.session.remove()

    @app.teardown_appcontext
    def shutdown_session2(exception=None):
        db.session.remove()

def create_app():
    '''Construct the core application'''
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.config['UPLOAD_FOLDER'] = basedir + '/static/uploads/'
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']

    register_extensions(app)
    register_blueprints(app)
    configure_database(app)

    return app