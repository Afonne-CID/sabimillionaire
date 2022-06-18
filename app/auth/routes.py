import imghdr
import os
from flask import render_template, redirect, request, url_for, current_app, abort
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from requests import head
from app import db, login_manager
from app.auth import blueprint
from app.auth.forms import LoginForm, CreateAccountForm
from ..models import User, Account, HeadShot
from app.auth.util import verify_pass
from werkzeug.utils import secure_filename

# UPLOAD_FOLDER = path + '/static/uploads'
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif']) #, 'pdf', 'png', 'jpg', 'jpeg', 'gif'


# Login & Registration
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:

        # read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = User.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):

            login_user(user)
            return redirect(url_for('home_blueprint.index'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    
    logout_user()
    create_account_form = CreateAccountForm(request.form)

    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        headshot = request.files['headshot']

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        user = User.query.filter_by(phone=phone).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Phone already registered',
                                   success=False,
                                   form=create_account_form)

        filename = secure_filename(headshot.filename)
        if not headshot or filename == '':
            return render_template('accounts/register.html',
                                   msg='Headshot is required',
                                   success=False,
                                   form=create_account_form)

        # file_name = secure_filename(headshot.filename)
        # mimetype = headshot.mimetype

        # else we can create the user
        try:       
            user = User(**request.form)
            db.session.add(user)
            db.session.flush()

            account = Account(user_id=user.id)

            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(headshot.stream):
                        abort(400)

            filename = '{}.{}'.format(user.username, file_ext)#secure_filename(headshot.filename)
            headshot.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            headshot = HeadShot(name='static/uploads/'+str(filename),
                            user_id=user.id)

            db.session.add(headshot)
            db.session.add(account)
            
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e

        return render_template('accounts/register.html',
                               msg='User created please <a href="/login">login</a>',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    # return redirect(url_for('auth_blueprint.login'))
    return redirect(url_for('auth_blueprint.login'))


# Errors
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')