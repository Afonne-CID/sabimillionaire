"""App entry point."""
from app import create_app
from app.models import *
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin

app = create_app()
admin = Admin(app)

# # Add model views
admin.add_view(UserView(User, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Users"))
admin.add_view(ModelView(JuniorSecondary, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Junior"))
admin.add_view(ModelView(SeniorSecondary, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Secondary"))
admin.add_view(ModelView(University, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="University"))
admin.add_view(ModelView(Account, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Accounts"))
admin.add_view(ModelView(Level, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="Levels"))
admin.add_view(AdminUserView(AdminUser, db.session, menu_icon_type='fa', menu_icon_value='fa-users', name="AdminUsers"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)