# -*- encoding: utf-8 -*-
import uuid
import requests
from urllib.parse import urlparse, parse_qs
from os import environ as env
from dotenv import load_dotenv
from app.home import blueprint
from app.home.forms import CreatePayment
from flask_login import current_user, logout_user
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from ..models import db, User #, Payment, UserPhoto
from urllib.parse import urlparse, parse_qs
from credo.payment import Payment as credo_payment


load_dotenv()


@blueprint.route('/')
def route_default():
    logout_user()
    return render_template('home/home.html')


@blueprint.route('/index')
@login_required
def index():
    
    return render_template(
            'home/index.html',
            segment='index',
            payments='',
            total_sent='',
            total_received='',
            total_deposit=''
        )


@blueprint.route('/<template>')
# @login_required
def route_template(template):

    try:
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.htm
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None

