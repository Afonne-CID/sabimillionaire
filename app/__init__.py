import os
from flask import Flask
from flask_admin.menu import MenuLink
from flask_admin import Admin
from flask_migrate import Migrate
from importlib import import_module
from app.models import *


basedir = os.path.abspath(os.path.dirname(__file__))

def register_extensions(app):
    db.init_app(app) # Initializes the database
    login_manager.init_app(app) #Initializes login manager
    migrate = Migrate(app, db)

def register_blueprints(app):
    for module_name in ('auth', 'home', 'transaction'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session2(exception=None):
        db.session.remove()

    @app.teardown_appcontext
    def shutdown_session2(exception=None):
        db.session.remove()

def create_app():
    '''Construct the core application'''
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('app.config.Config')
    
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)


    admin = Admin(app,
        'Dashboard',
        endpoint='/restricted/admin',
        url='/restricted/admin',
        template_mode='bootstrap4'
    )

    with app.app_context():
    
        try:
            withdrawal_requests = None
            deposit_requests = None
            total_users = None

            levels = Level.query.all()
            if len(levels) < 5:
                if len(levels) > 0:
                    for level in levels:
                        db.session.delete(level)
                    db.session.commit()

                res = [
                    Level(amount=1500),
                    Level(amount=5000),
                    Level(amount=15000),
                    Level(amount=25000),
                    Level(amount=50000)
                ]
                
                for level in res:
                    db.session.add(level)
                db.session.commit()

            withdrawal_requests = len(Withdraw.query.all())
            deposit_requests = len(Deposit.query.all())
            total_users = len(User.query.all())

            user_role = Role.query.filter_by(name='user').first()
            admin_role = Role.query.filter_by(name='admin').first()
            site_settings = SiteSettings.query.first()

            if not site_settings:
                site_settings = SiteSettings()
                db.session.add(site_settings)
            if not user_role:
                user_role = Role(name='user')
                db.session.add(user_role)
            if not admin_role:
                admin_role = Role(name='admin')
                db.session.add(admin_role)

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e


    # # Add model views
    admin.add_view(RolesView(Role, db.session, users=total_users, withdrawals=withdrawal_requests, deposits=deposit_requests, menu_icon_type='fa', menu_icon_value='fa-sitemap', name="Roles", roles_accepted=['admin']))
    admin.add_view(UserView(User, db.session, users=total_users, withdrawals=withdrawal_requests, deposits=deposit_requests, menu_icon_type='fa', menu_icon_value='fa-users', name="Users", roles_accepted=['admin']))
    admin.add_view(PrimaryView(Primary, db.session, users=total_users, withdrawals=withdrawal_requests, deposits=deposit_requests, menu_icon_type='fa', menu_icon_value='fa-book', name="Primary", roles_accepted=['admin']))
    admin.add_view(JuniorSecondaryView(JuniorSecondary, db.session, users=total_users, withdrawals=withdrawal_requests, deposits=deposit_requests, menu_icon_type='fa', menu_icon_value='fa-book', name="Junior", roles_accepted=['admin']))
    admin.add_view(SeniorSecondaryView(SeniorSecondary, db.session, users=total_users, withdrawals=withdrawal_requests, deposits=deposit_requests, menu_icon_type='fa', menu_icon_value='fa-book', name="Secondary", roles_accepted=['admin']))
    admin.add_view(UniversityView(University, db.session, users=total_users, withdrawals=withdrawal_requests, deposits=deposit_requests, menu_icon_type='fa', menu_icon_value='fa-book', name="University", roles_accepted=['admin']))
    admin.add_view(AccountView(Account, db.session, users=total_users, withdrawals=withdrawal_requests, deposits=deposit_requests, menu_icon_type='fa', menu_icon_value='fa-id-card-o', name="Accounts", roles_accepted=['admin']))
    admin.add_view(LevelView(Level, db.session, users=total_users, withdrawals=withdrawal_requests, deposits=deposit_requests, menu_icon_type='fa', menu_icon_value='fa-level-up', name="Levels", roles_accepted=['admin']))
    admin.add_view(WithdrawView(Withdraw, db.session, users=total_users, withdrawals=withdrawal_requests, deposits=deposit_requests, menu_icon_type='fa', menu_icon_value='fa-university', name="Withdrawals", roles_accepted=['admin']))
    admin.add_view(DepositView(Deposit, db.session, users=total_users, withdrawals=withdrawal_requests, deposits=deposit_requests, menu_icon_type='fa', menu_icon_value='fa-credit-card-alt', name="Deposits", roles_accepted=['admin']))
    admin.add_link(MenuLink(name='Logout', category='', url="/logout"))
    admin.add_link(MenuLink(name='Login', category='', url="/login"))

    return app