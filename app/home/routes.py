# -*- encoding: utf-8 -*-
import uuid
import requests
from urllib.parse import urlparse, parse_qs
from os import environ as env
from dotenv import load_dotenv
from app.home import blueprint
from app.home.forms import CreatePayment
from flask_login import current_user, logout_user
from flask import redirect, render_template, request, url_for, jsonify
from flask_login import login_required
from jinja2 import TemplateNotFound
from ..models import *
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import random
import time


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

@blueprint.route('/free-trivia', methods=['GET', 'POST'])
@login_required
def free_trivia():

    id = current_user.get_id()

    if request.method == 'POST':
        if 'start' in request.form:
            cur_level = 1
            cnt = 0

        if 'next' in request.form:
            cur_level = int(request.form['level'])
            cnt = int(request.form['cnt'])
            question_id = request.form['question-id']
            option_selected = request.form.get('unique-selection', None)

            if cnt == 5:
                reward = Level.query.get(cur_level).amount

        age = age_calculator(User.query.get(id).dob)
        base_table = db_table_selector(age)
        if cur_level > 1:
            base_table = db_table_next(base_table)
    
        q_list = list(Attempt.query.filter(Attempt.user_id==id))
        questions_in_db = len(base_table.query.all())

        comp = 5
        if questions_in_db < 5:
            comp = questions_in_db

        if cnt + 1 <= comp:
            
            cnt += 1

            tmp = random.randint(0, questions_in_db)

            try:
                question = base_table.query.get(tmp)
                while not question or tmp in q_list:
                    tmp = random.randint(0, questions_in_db)
                    if tmp not in q_list:
                        question = base_table.query.get(tmp)
                
                if cnt + 1 == comp:
                    cur_level += 1

                options = shuffle_list([question.correct_option,
                                            question.wrong_option1,
                                            question.wrong_option2,
                                            question.wrong_option3,
                                            question.wrong_option4])

                return render_template(
                    'home/questions.html',
                    level=cur_level,
                    question=question,
                    options=options,
                    cnt=cnt
                )

            except Exception as e:
                '''
                '''
                return e

                
    elif request.method == 'GET':
        level = 1
        return render_template(
                'home/questions.html',
                level=level
        )


@blueprint.route('/play-and-win', methods=['GET'])
@login_required
def play_and_win():
    '''
    '''
    return render_template(
        'home/questions.html'
    )


@blueprint.route('/<template>')
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


def age_calculator(born):
    today = datetime.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def db_table_selector(age):
    if 12 <= age <= 14:
        return JuniorSecondary
    if 15 <= age <= 18:
        return SeniorSecondary
    if 18 <= age <= 45:
        return University

def db_table_next(table_name):
    if table_name == JuniorSecondary:
        return SeniorSecondary
    elif table_name == SeniorSecondary:
        return University
    else:
        return University

def shuffle_list(list):
     for i in range(len(list)):   
             j = random.randint(0,len(list)-1)
             list[i], list[j] = list[j], list[i]
     return list