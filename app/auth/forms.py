# -*- encoding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired

# login and registration
class LoginForm(FlaskForm):
    username = StringField('Username',
                         id='username_login',
                         validators=[DataRequired()])
    password = PasswordField('Password',
                             id='pwd_login',
                             validators=[DataRequired()])


class CreateAccountForm(FlaskForm):
    headshot = FileField('Your headshot',
                         id='headshot',
                         validators=[DataRequired()])
    username = StringField('Username',
                         id='username_create',
                         validators=[DataRequired()])
    email = StringField('Email',
                      id='email_create',
                      validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             id='pwd_create',
                             validators=[DataRequired()])
    first_name = StringField('First Name',
                            id='first_name',
                            validators=[DataRequired()])
    last_name = StringField('First Name',
                            id='last_name',
                            validators=[DataRequired()])
    dob = StringField('Date of Birth',
                            id='dob',
                            validators=[DataRequired()])
    phone = StringField('Phone',
                        id='phone',
                        validators=[DataRequired()])