from flask import (redirect,
                    render_template,
                    request,
                    url_for)
from flask_login import (login_required,
                        login_user,
                        current_user)
from app.admin import blueprint
from app.admin.forms import LoginForm
from app.models import Admin
from app.auth.util import verify_pass

# @blueprint.route('/restricted/admin/', methods=['GET', 'POST'])
# @login_required
# def restricted():
#     ''''''
#     return render_template('admin/index.html')

@blueprint.route('/restricted/login', methods=['GET', 'POST'])
def restricted_login():
    ''''''
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username).first()
        if admin and verify_pass(password, admin.password):
            ''''''
            login_user(admin)

        return render_template('admin/login.html',
                            msg='Wrong user or password',
                            form=login_form)

    if not current_user.is_authenticated:
        return render_template('admin/login.html',
                               form=login_form)
#     return render_template('admin/index.html')