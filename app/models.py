import datetime
from enum import unique
from flask import abort, redirect, url_for, request
from distutils.command.build_scripts import first_line_re
from doctest import debug_script
from email.policy import default
from flask_admin import expose, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, UserMixin, logout_user
from flask_security import RoleMixin
from flask_sqlalchemy import SQLAlchemy
from app.auth.util import hash_pass as hp
from wtforms import PasswordField
from flask_security.forms import LoginForm


db = SQLAlchemy()
login_manager = LoginManager()


class Roled(RoleMixin):
    @login_manager.user_loader
    def is_accessible(self):
        user = current_user
        try:
            if user.has_role('admin'):
                return True
            return False
        except Exception as e:
            abort(403)

    def _handle_view(self, name, *args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('security.login'))
            # return redirect(url_for('admin_blueprint.restricted_login'))
        if not self.is_accessible():
            # return self.render("admin/denied.html")
            return "<p>Access denied</p>"

class AdminView(Roled, ModelView):

    def __init__(self, *args, **kwargs):
        self.roles_accepted = kwargs.pop('roles_accepted', list())
        super(AdminView, self).__init__(*args, **kwargs)

        # return self.render('admin/index.html')

class MyAdminIndexView(AdminIndexView):
    pass
    # def index(self):
    #     if not current_user.is_authenticated:
    #         next_url = request.url
    #         login_url = '%s?next=%s' % (url_for('login'), next_url)
    #         return redirect(login_url)
    #     return super(self, MyAdminIndexView).index()


class UserView(AdminView):
    column_exclude_list = ['password']

class PrimaryView(AdminView):
    pass

class JuniorSecondaryView(AdminView):
    pass

class SeniorSecondaryView(AdminView):
    pass

class UniversityView(AdminView):
    pass

class AccountView(AdminView):
    pass

class LevelView(AdminView):
    pass

class WithdrawView(AdminView):
    pass

class DepositView(AdminView):
    pass

class RolesView(AdminView):
    pass

class RolesUsers(AdminView):
    pass

####################################################
# Models
####################################################


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class SiteSettings(db.Model, UserMixin):
    __table__name = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)
    min_withdraw = db.Column(db.Integer, default=1500)
    cost_per_slot = db.Column(db.Integer, default=200)
    email = db.Column(db.String(50), default='info@sabimillionaire.com.ng')
    phone = db.Column(db.String(13))
    address = db.Column(db.String(250))
    site_name = db.Column(db.String(50), default='Sabimillionaire')

class GrandWinner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grand_winner = db.Column(db.String(50), default=None)
    grand_winner_time = db.Column(db.DateTime, default=None)


class User(db.Model, UserMixin):
    '''User table
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(13))
    dob = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime)
    address = db.Column(db.String(250))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    password = db.Column(db.String(255), nullable=False)
    verify = db.Column(db.String(50))
    status = db.Column(db.Integer, default=9)
    active = db.Column(db.Boolean, default=False)
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('user', lazy='dynamic'))

    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})


    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hp(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    # def __repr__(self):
    #     return str(self.username)

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None


class Primary(db.Model):
    __tablename__ = 'primary'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    question = db.Column(db.String(250), nullable=False)
    correct_option = db.Column(db.String(250), nullable=False)
    wrong_option1 = db.Column(db.String(250), nullable=False)
    wrong_option2 = db.Column(db.String(250), nullable=False)
    wrong_option3 = db.Column(db.String(250), nullable=False)
    wrong_option4 = db.Column(db.String(250), nullable=False)


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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_correct = db.Column(db.Integer, default=0)
    total_failed = db.Column(db.Integer, default=0)
    total_attempted = db.Column(db.Integer, default=0)
    slots = db.Column(db.Integer, default=0)
    coin_balance = db.Column(db.Integer, default=0)
    wallet_balance = db.Column(db.Float, default=0.0)


class Level(db.Model):
    __tablename__ = 'levels'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    amount = db.Column(db.Integer, nullable=False)


class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    user_selection = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)


class Countries(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    two_char = db.Column(db.String(10), nullable=False)
    three_char = db.Column(db.String(10), nullable=False)


class HeadShot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), default='static/uploads/default-avatar.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Deposit(db.Model):
    '''Represents the payment table
    '''
    id = db.Column(db.Integer, primary_key=True, unique=True)
    status = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    reference = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    paid_at = db.Column(db.DateTime, nullable=False)
    payment_option = db.Column(db.String(50), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Withdraw(db.Model):
    '''Represents the payment table
    '''
    id = db.Column(db.Integer, primary_key=True, unique=True)
    status = db.Column(db.String(10), nullable=False, default='Pending')
    amount = db.Column(db.Float, nullable=False)
    reference = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    bank_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.Integer, nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)