import uuid
from flask import Flask, jsonify, abort, current_app, render_template
from flask_mail import Mail, Message
from app.models import db, SiteSettings


def mailer(to, subject, template, user):
    app = current_app
    site_settings = SiteSettings.query.first()
    site_logo = '/static/assets/images/logo.png'

    with app.app_context():
        mail = Mail(app)
        msg = Message(subject, sender=site_settings.email, recipients=to)

        if template == 'register':
            msg.html = render_template('mail/registration.html',
                                        site_logo=site_logo,
                                        user_first_name=user.first_name,
                                        otp=user.verify,
                                        user_email=user.email,
                                        admin_email=site_settings.email,
                                        site_name=site_settings.site_name)
        else:

            otp = generate_code()
            user.verify = otp
            db.session.commit()

            if template == 'reset-password':
                ''''''
                msg.html = render_template('mail/reset-password.html',
                            site_logo=site_logo,
                            user_first_name=user.first_name,
                            otp=otp,
                            user_email=user.email,
                            admin_email=site_settings.email,
                            site_name=site_settings.site_name)
            else:
                msg.html = render_template('mail/send-otp.html',
                                            site_logo=site_logo,
                                            user_first_name=user.first_name,
                                            otp=otp,
                                            user_email=user.email,
                                            admin_email=site_settings.email,
                                            site_name=site_settings.site_name)
        try:
            mail.send(msg)

        except Exception as e:
            raise e
        
        return

def generate_code():
    ''''''
    val = str(uuid.uuid4()).split('-')
    return '{}'.format(val[1].upper())