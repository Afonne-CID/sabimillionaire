import os
from flask import Flask, url_for, redirect, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_migrate import Migrate
from flask_admin.contrib import sqla
from flask_admin import helpers as admin_helpers
from flask_admin import BaseView, expose
from wtforms import PasswordField

# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/sabimil'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('admin_user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class AdminUser(db.Model, UserMixin):
    __tablename__ = 'admin_user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('admin_user', lazy='dynamic'))

    def __str__(self):
        return self.email


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, AdminUser, Role)
security = Security(app, user_datastore)


# Create customized model view class
class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('superuser'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


    # can_edit = True
    edit_modal = True
    create_modal = True    
    can_export = True
    can_view_details = True
    details_modal = True

class UserView(MyModelView):
    column_editable_list = ['email', 'first_name', 'last_name']
    column_searchable_list = column_editable_list
    column_exclude_list = ['password']
    #form_excluded_columns = column_exclude_list
    column_details_exclude_list = column_exclude_list
    column_filters = column_editable_list
    form_overrides = {
        'password': PasswordField
    }


class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('my_master.html')

# Flask views
@app.route('/')
def index():
    return redirect(url_for('security.login'))

@app.route('/admin')
def admin():
    return redirect(url_for('security.login'))


# Create admin
admin = flask_admin.Admin(
    app,
    'My Dashboard',
    base_template='my_master.html',
    template_mode='bootstrap4',
)

# Add model views
admin.add_view(MyModelView(Role, db.session, menu_icon_type='fa', menu_icon_value='fa-server', name="Roles"))
admin.add_view(UserView(AdminUser, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Users"))
admin.add_view(CustomView(name="Custom view", endpoint='custom', menu_icon_type='fa', menu_icon_value='fa-connectdevelop',))

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

def build_sample_db():
    with app.app_context():
        user_role = Role(name='user')
        super_user_role = Role(name='superuser')
        db.session.add(user_role)
        db.session.add(super_user_role)
        db.session.commit()

        test_user = user_datastore.create_user(
            first_name='Admin',
            email='admin',
            password=encrypt_password('admin'),
            roles=[user_role, super_user_role]
        )

    db.session.add(test_user)
    db.session.commit()

    return

if __name__ == '__main__':

    # # Build a sample db on the fly, if one does not exist yet.
    # app_dir = os.path.realpath(os.path.dirname(__file__))
    # database_path = os.path.join(app_dir, app.config['DATABASE_FILE'])
    
    # build_sample_db()

    # Start app
    app.run(debug=True)
