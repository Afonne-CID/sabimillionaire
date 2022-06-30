"""App entry point."""
from app import create_app
from app.models import *
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin


app = create_app()
admin = Admin(app,
    'Dashboard',
    endpoint='/restricted/admin',
    url='/restricted/admin',
    template_mode='bootstrap4'
)

# # Add model views
admin.add_view(UserView(User, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Users"))
admin.add_view(ModelView(Primary, db.session, menu_icon_type='fa', menu_icon_value='fa-book', name="Primary"))
admin.add_view(ModelView(JuniorSecondary, db.session, menu_icon_type='fa', menu_icon_value='fa-book', name="Junior"))
admin.add_view(ModelView(SeniorSecondary, db.session, menu_icon_type='fa', menu_icon_value='fa-book', name="Secondary"))
admin.add_view(ModelView(University, db.session, menu_icon_type='fa', menu_icon_value='fa-book', name="University"))
admin.add_view(ModelView(Account, db.session, menu_icon_type='fa', menu_icon_value='fa-id-card-o', name="Accounts"))
admin.add_view(ModelView(Level, db.session, menu_icon_type='fa', menu_icon_value='fa-level-up', name="Levels"))
admin.add_view(ModelView(Withdraw, db.session, menu_icon_type='fa', menu_icon_value='fa-university', name="Withdrawals"))
admin.add_view(ModelView(Deposit, db.session, menu_icon_type='fa', menu_icon_value='fa-credit-card-alt', name="Deposits"))
# admin.add_view(AdminUserView(AdminUser, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="AdminUsers"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)