from doctest import debug_script
import mimetypes
from . import db
from flask_login import UserMixin
from app import db, login_manager
from app.auth.util import hash_pass
import datetime


class User(db.Model, UserMixin):
    '''User table
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    dob = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime)
    address = db.Column(db.String(250))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    password = db.Column(db.LargeBinary)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None


class Transaction(db.Model):
    '''Represents the payment table
    '''
    id = db.Column(db.Integer, primary_key=True, unique=True)
    status = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    reference = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime)
    payment_option = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class JuniorSecondary(db.Model):
    __tablename__ = 'junior_secondary'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    question = db.Column(db.String(250), nullable=False)
    correct_option = db.Column(db.String(250), nullable=False)
    wrong_option1 = db.Column(db.String(250), nullable=False)
    wrong_option2 = db.Column(db.String(250), nullable=False)
    wrong_option3 = db.Column(db.String(250), nullable=False)
    wrong_option4 = db.Column(db.String(250), nullable=False)
    

class SeniorSecondary(db.Model):
    __tablename__ = 'senior_secondary'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    question = db.Column(db.String(250), nullable=False)
    correct_option = db.Column(db.String(250), nullable=False)
    wrong_option1 = db.Column(db.String(250), nullable=False)
    wrong_option2 = db.Column(db.String(250), nullable=False)
    wrong_option3 = db.Column(db.String(250), nullable=False)
    wrong_option4 = db.Column(db.String(250), nullable=False)


class University(db.Model):
    __tablename__ = 'university'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    question = db.Column(db.String(250), nullable=False)
    correct_option = db.Column(db.String(250), nullable=False)
    wrong_option1 = db.Column(db.String(250), nullable=False)
    wrong_option2 = db.Column(db.String(250), nullable=False)
    wrong_option3 = db.Column(db.String(250), nullable=False)
    wrong_option4 = db.Column(db.String(250), nullable=False)

class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    total_correct = db.Column(db.Integer)
    total_failed = db.Column(db.Integer)
    total_attempted = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Level(db.Model):
    __tablename__ = 'levels'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    amount = db.Column(db.Integer, nullable=False)

class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, unique=True, nullable=False)
    user_selection = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)