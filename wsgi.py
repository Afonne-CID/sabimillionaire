"""App entry point."""
import os
import hashlib
import binascii
from app import create_app
from app.models import *
from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security.utils import encrypt_password
from flask_admin import Admin as Adm, helpers as admin_helpers


app = create_app()

admin = Adm(app,
    'Dashboard',
    endpoint='/restricted/admin',
    url='/restricted/admin',
    template_mode='bootstrap4',
    # index_view=DashboardView()
    # base_template='admin/my_master.html'
)


# # Add model views
admin.add_view(RolesView(Role, db.session, menu_icon_type='fa', menu_icon_value='fa-sitemap', name="Roles", roles_accepted=['admin']))
admin.add_view(UserView(User, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Users", roles_accepted=['admin']))
admin.add_view(PrimaryView(Primary, db.session, menu_icon_type='fa', menu_icon_value='fa-book', name="Primary", roles_accepted=['admin']))
admin.add_view(JuniorSecondaryView(JuniorSecondary, db.session, menu_icon_type='fa', menu_icon_value='fa-book', name="Junior", roles_accepted=['admin']))
admin.add_view(SeniorSecondaryView(SeniorSecondary, db.session, menu_icon_type='fa', menu_icon_value='fa-book', name="Secondary", roles_accepted=['admin']))
admin.add_view(UniversityView(University, db.session, menu_icon_type='fa', menu_icon_value='fa-book', name="University", roles_accepted=['admin']))
admin.add_view(AccountView(Account, db.session, menu_icon_type='fa', menu_icon_value='fa-id-card-o', name="Accounts", roles_accepted=['admin']))
admin.add_view(LevelView(Level, db.session, menu_icon_type='fa', menu_icon_value='fa-level-up', name="Levels", roles_accepted=['admin']))
admin.add_view(WithdrawView(Withdraw, db.session, menu_icon_type='fa', menu_icon_value='fa-university', name="Withdrawals", roles_accepted=['admin']))
admin.add_view(DepositView(Deposit, db.session, menu_icon_type='fa', menu_icon_value='fa-credit-card-alt', name="Deposits", roles_accepted=['admin']))
admin.add_link(MenuLink(name='Logout', category='', url="/logout"))
admin.add_link(MenuLink(name='Login', category='', url="/login"))
# admin.add_view(Logout(name="Logout"))
# admin.add_link(LoginMenuLink(name='Login', category='', url="/login"))
# admin.add_view(AdminUserView(AdminUser, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="AdminUsers"))

# salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
# app.config['SECURITY_PASSWORD_SALT'] = salt

# user_datastore = SQLAlchemyUserDatastore(db, Admin, Role)
# security = Security(app, user_datastore)

# def build_sample_db():
#     with app.app_context():
#         admin_username = 'for_admin'#app.config['ADMIN_USERNAME']
#         admin_pwd = app.config['ADMIN_PWD']
#         user = User.query.filter_by(username=admin_username).first()
#         user_role = Role.query.filter_by(name='user').first()
#         admin_role = Role.query.filter_by(name='admin').first()
#         site_settings = SiteSettings.query.first()
        
#         try:
#             if not site_settings:
#                 site_settings = SiteSettings()
#                 db.session.add(site_settings)
#             if not user_role:
#                 user_role = Role(name='user')
#                 db.session.add(user_role)
#             if not admin_role:
#                 admin_role = Role(name='admin')
#                 db.session.add(admin_role)

#             if not user:

#                     user = user_datastore.create_user(
#                             username='for_admin',#admin_username,
#                             password='admin',#admin_pwd, #hash_pass(admin_pwd),
#                             first_name='admin',
#                             last_name='admin',
#                             email='for_admin@gmail.com',
#                             phone='+234-807',
#                             dob=datetime.today(),
#                             verify='AJS7',
#                             status=1,
#                             active=True
#                     )
#                     # user.password = admin_pwd
#                     user.roles = [admin_role]
#                     db.session.add(user)
        
#             db.session.commit()

#         except Exception as e:
#             db.session.rollback()
#             raise e

#     return

if __name__ == "__main__":
    # build_sample_db()
    app.run(host="0.0.0.0", port=5000)