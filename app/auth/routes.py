import imghdr
import os
import uuid
from flask import (
    render_template,
    redirect,
    request,
    url_for,
    current_app, abort,
    flash)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from app import db, login_manager
from app.mail.mailer import mailer
from app.auth import blueprint
from app.auth.forms import (
    LoginForm,
    CreateAccountForm,
    VerifyAccount,
    ChangePassword
)
from ..models import User, Account, HeadShot, Role
from app.auth.util import verify_pass, hash_pass
from werkzeug.utils import secure_filename


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
            if user.status == 1 and user.active:
                return redirect(url_for('home_blueprint.index'))
            elif user.status == 9:
                mailer([user.email], 'Verification Code', '', user)
                return redirect(url_for('auth_blueprint.verify_account'))
            else:
                return render_template('accounts/account-blocked.html')

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html',
                               form=login_form)
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/verify-otp', methods=['GET', 'POST'])
@login_required
def verify_account():

    id = current_user.get_id()
    user = User.query.get(id)
    verify_form = VerifyAccount(request.form)

    if request.method == 'POST':
        ''''''
        if 'verification' in request.form:
            input_otp = request.form['otp']
            correct_otp = user.verify

            if input_otp == correct_otp:
                flash('Verification successful')
                user.status, user.active = 1, 1
                db.session.commit()
                return redirect(url_for('home_blueprint.index'))
        
            return render_template('accounts/verify-account.html',
                            msg='Invalid OTP supplied',
                            form=verify_form)

        if 'resend-otp' in request.form:
            ''''''
            mailer([user.email], 'New OTP', '', user)
            flash('Otp has been resent')

    return render_template('accounts/verify-account.html', form=verify_form)

@blueprint.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    ''''''
    try:
        change_password = ChangePassword(request.form)
    except Exception as e:
        print(e)
        pass

    if request.method == 'POST':
        if 'verification' in request.form:
            email = request.form['email']
            if not email:
                flash('Email is required')
            else:
                user = User.query.filter_by(email=email).first()
                if not user:
                    flash("No user with that email was found")
                else:
                    mailer([user.email], 'New OTP', 'reset-password', user)
                    return render_template('accounts/reset-password.html',
                    form=change_password, status=True,
                    email=email)

        if 'reset-password' in request.form:
            input_otp = request.form['otp']
            email = request.form['email']
            new_password = hash_pass(request.form['new_password'])

            user = User.query.filter_by(email=email).first()
            if not user:
                flash("No user with that email was found")
            else:
                correct_otp = user.verify
                if input_otp == correct_otp:
                    flash('Password change successful')
                    user.password = new_password
                    db.session.commit()
                    login_user(user)
                    return redirect(url_for('home_blueprint.index'))
                else:
                    flash('Invalid OTP supplied')
                    return render_template('accounts/reset-password.html',
                                            form=change_password, status=True, email=email)
        
        return render_template('accounts/reset-password.html', form=change_password)

    else:
        return render_template('accounts/reset-password.html')

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
        try:

            user_role = Role.query.filter_by(name='user').first()

            user = User(**request.form)
            user.verify = generate_code()
            user.roles = [user_role]
            db.session.add(user)
            db.session.flush()

            account = Account(user_id=user.id)

            if filename:
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in current_app.config['UPLOAD_EXTENSIONS'] or \
                        file_ext != validate_image(headshot.stream):
                            abort(400)

                filename = '{}.{}'.format(user.username, file_ext)
                headshot.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

                headshot = HeadShot(name='static/uploads/'+str(filename),
                                user_id=user.id)
                                
                db.session.add(headshot)
            else:
                headshot = HeadShot(user_id=user.id)
            
            db.session.add(headshot)
            db.session.add(account)

            login_user(user)
            db.session.commit()

            mailer([user.email], 'Registration Was Successful', 'register', user)

        except Exception as e:
            db.session.rollback()
            print(e)

            return render_template('accounts/register.html',
                                msg='Error occured',
                                success=False,
                                form=create_account_form)

        # return render_template('accounts/register.html',
        #             msg='User created please <a href="/login">login</a>',
        #             success=True,
        #             form=create_account_form)
        return redirect(url_for('auth_blueprint.verify_account'))

    else:
        return render_template('accounts/register.html', form=create_account_form)

@blueprint.route('/logout')
def logout():
    logout_user()
    # return redirect(url_for('auth_blueprint.login'))
    return redirect(url_for('home_blueprint.route_default'))

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

def generate_code():
    ''''''
    val = str(uuid.uuid4()).split('-')
    return '{}'.format(val[1].upper())

def allow_access(current_user):

    user_id = current_user.get_id()
    user = User.query.get(user_id)

    if not (user.active and user.status == 1):
        abort(403)