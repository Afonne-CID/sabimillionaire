# -*- encoding: utf-8 -*-
import uuid
import requests
from urllib.parse import urlparse, parse_qs
from os import environ as env
from dotenv import load_dotenv
from app.home import blueprint
from app.home.forms import CreatePayment
from flask_login import current_user, logout_user
from app.auth.util import hash_pass
from flask import redirect, render_template, request, url_for, jsonify, abort, flash
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
    
    id = current_user.get_id()
    account = Account.query.filter_by(user_id=id).first()
    grade = grade_finder(account.total_correct, account.total_attempted)

    return render_template(
            'home/index.html',
            segment='index',
            wallet_balance=account.wallet_balance,
            total_correct=account.total_correct,
            total_failed=account.total_failed,
            total_attempted=account.total_attempted,
            slots=account.slots,
            coin_balance=account.coin_balance,
            grade=grade
        )


@blueprint.route('/play-game', methods=['POST', 'GET'])
@login_required
def play_game():
    
    if request.method == 'GET':
        level = 0
        return render_template(
                'home/questions.html',
                level=level
        )
    
    # if request.method == 'POST':
    #     if 'trivia-test' in request.form:
    #         return redirect(url_for('home_blueprint.free_trivia', form=request.form))
    #     if 'play-n-win' in request.form:
    #         return redirect(url_for('home_blueprint.play_and_win', form=request.form))


@blueprint.route('/free-trivia', methods=['POST', 'GET'])
@login_required
def free_trivia():

    id = current_user.get_id()

    if request.method == 'POST':
        try:
            age = age_calculator(User.query.get(id).dob)
            base_table = db_table_selector(age)

            if 'next-level' in request.form:
                cur_level = int(request.form['level'])
                cnt = int(request.form['cnt'])

                if cur_level >= 6:
                    return render_template('home/index.html')

            if 'cashout' in request.form:
                reward = 10
                account = Account.query.filter_by(user_id=id).first()
                account.coin_balance += reward

                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    raise e

                return render_template('home/index.html')

            if 'start' in request.form:
                cur_level = 0
                cnt = 0

            if 'next' in request.form:
                cur_level = int(request.form['level'])
                cnt = int(request.form['cnt'])
                question_id = request.form['question-id']
                user_selection = request.form.get('unique-selection', '')
                
                attempt = Attempt(user_id=id,
                                question_id=question_id,
                                user_selection=user_selection,
                                category=base_table.__name__)

                try:
                    db.session.add(attempt)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(e)
                    abort(500)
        
            if cur_level > 1:
                base_table = db_table_next(base_table)

            '''Will increase the limite to 100 later'''
            q_list = [attempt.question_id for attempt in Attempt.query.\
                    filter(Attempt.user_id==id).\
                    order_by(Attempt.created_at.desc()).limit(2).all()]

            questions_in_db = len(base_table.query.all())

            comp = 5
            if questions_in_db < 5:
                comp = questions_in_db

            if cnt + 1 <= comp:
                
                cnt += 1

                tmp = random.randint(0, questions_in_db)

                question = base_table.query.get(tmp)
                while not question or tmp in q_list:

                    tmp = random.randint(0, questions_in_db)
                    if tmp not in q_list:
                        question = base_table.query.get(tmp)
                
                if cnt == comp:
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

            else:
                '''Display result'''
                reward = Level.query.get(cur_level).amount

                attempts = Attempt.query.filter(Attempt.user_id==id).\
                    order_by(Attempt.created_at.desc()).limit(5).all()

                all_questions = []
                passed = 0
                for attempt in attempts:
                    question_id = attempt.question_id
                    user_selection = attempt.user_selection
                    category = eval(attempt.category.split('.')[-1].strip('>\''))
                    question = category.query.get(question_id)
                    each_question = []

                    if user_selection == question.correct_option:
                        passed += 1
                    
                    options = shuffle_list([question.correct_option,
                                            question.wrong_option1,
                                            question.wrong_option2,
                                            question.wrong_option3,
                                            question.wrong_option4])

                    each_question.append(question.question)
                    each_question.append(question.correct_option)
                    each_question.append(user_selection)
                    each_question.append(options)
                    all_questions.append(each_question)

                account = Account.query.filter_by(user_id=id).first()
                account.total_correct += passed
                account.total_failed += comp - passed
                account.total_attempted += cnt

                db.session.commit()

                if passed != comp:
                    return render_template(
                        'home/answers.html',
                        all_questions=all_questions,
                        level=cur_level,
                        won=False,
                        passed=passed,
                        question=question,
                        options=options,
                        cnt=cnt
                    )

                else:
                    return render_template(
                        'home/questions.html',
                        level=cur_level,
                        won=True,
                        reward=reward,
                        # question=question,
                        # options=options,
                        cnt=cnt
                    )

        except Exception as e:
            '''
            '''
            raise Exception(e)       



@blueprint.route('/play-and-win', methods=['POST', 'GET'])
@login_required
def play_and_win():

    id = current_user.get_id()
    account = Account.query.filter_by(user_id=id).first()
    attempts_left = account.slots

    if request.method == 'POST':
        try:
            age = age_calculator(User.query.get(id).dob)
            base_table = db_table_selector(age)

            if 'next-level' in request.form:
                cur_level = int(request.form['level'])
                cnt = int(request.form['cnt'])

                if cur_level >= 6:
                    return render_template('home/index.html')

            if 'cashout' in request.form:
                reward = float(request.form['reward'])
                account.wallet += reward

                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    raise e

                return render_template('home/index.html')

            if 'start' in request.form:

                if attempts_left <= 0:
                    flash('no attempts left')
                    return redirect(url_for('home_blueprint.index'))
                else:
                    account.slots -= 1
                    db.session.commit()

                    cur_level = 0
                    cnt = 0

            if 'next' in request.form:
                cur_level = int(request.form['level'])
                cnt = int(request.form['cnt'])
                question_id = request.form['question-id']
                user_selection = request.form.get('unique-selection', '')
                
                attempt = Attempt(user_id=id,
                                question_id=question_id,
                                user_selection=user_selection,
                                category=base_table.__name__)

                try:
                    db.session.add(attempt)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(e)
                    abort(500)
        
            if cur_level > 1:
                base_table = db_table_next(base_table)

            '''Will increase the limite to 100 later'''
            q_list = [attempt.question_id for attempt in Attempt.query.\
                    filter(Attempt.user_id==id).\
                    order_by(Attempt.created_at.desc()).limit(2).all()]

            questions_in_db = len(base_table.query.all())

            comp = 5
            if questions_in_db < 5:
                comp = questions_in_db

            if cnt + 1 <= comp:
                
                cnt += 1

                tmp = random.randint(0, questions_in_db)

                question = base_table.query.get(tmp)
                while not question or tmp in q_list:

                    tmp = random.randint(0, questions_in_db)
                    if tmp not in q_list:
                        question = base_table.query.get(tmp)
                
                if cnt == comp:
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

            else:
                '''Display result'''
                reward = Level.query.get(cur_level).amount

                attempts = Attempt.query.filter(Attempt.user_id==id).\
                    order_by(Attempt.created_at.desc()).limit(5).all()

                all_questions = []
                passed = 0
                for attempt in attempts:
                    question_id = attempt.question_id
                    user_selection = attempt.user_selection
                    category = eval(attempt.category.split('.')[-1].strip('>\''))
                    question = category.query.get(question_id)
                    each_question = []

                    if user_selection == question.correct_option:
                        passed += 1
                    
                    options = shuffle_list([question.correct_option,
                                            question.wrong_option1,
                                            question.wrong_option2,
                                            question.wrong_option3,
                                            question.wrong_option4])

                    each_question.append(question.question)
                    each_question.append(question.correct_option)
                    each_question.append(user_selection)
                    each_question.append(options)
                    all_questions.append(each_question)

                account = Account.query.filter_by(user_id=id).first()
                account.total_correct += passed
                account.total_failed += comp - passed
                account.total_attempted += cnt

                db.session.commit()

                if passed != comp:
                    return render_template(
                        'home/answers.html',
                        all_questions=all_questions,
                        level=cur_level,
                        won=False,
                        paid=True,
                        attempts_left=attempts_left,
                        passed=passed,
                        question=question,
                        options=options,
                        cnt=cnt
                    )

                else:
                    return render_template(
                        'home/questions.html',
                        level=cur_level,
                        won=True,
                        reward=reward,
                        # question=question,
                        # options=options,
                        cnt=cnt
                    )

        except Exception as e:
            '''
            '''
            raise Exception(e) 

@blueprint.route('page-profile', methods=['POST', 'GET'])
def page_profile():
    ''''''
    id = current_user.get_id()
    user = User.query.get(id)

    if request.method == 'GET':
        return render_template('home/page-profile.html',
            filename=HeadShot.query.filter_by(user_id=id).first().name,
            full_name='{} {}'.format(user.first_name, user.last_name),
            username=user.username,
            email=user.email,
            phone=user.phone,
            countries=Countries.query.all()
        )
    
    elif request.method == 'POST':

        try:
            if request.form['full_name']:
                name = request.form['full_name'].split(' ')
                if name and len(name) > 1:
                    user.first_name = name[0]
                    user.last_name = name[1]
            if request.form['password']:
                password = hash_pass(request.form['password'])
                user.password = password
            if request.form['email']:
                user.email = request.form['email']
            if request.form['phone']:
                user.phone = request.form['phone']
            if request.form['country']:
                user.country = request.form['country']
            
            db.session.commit()
        
        except Exception as e:
            db.session.rollback()
            raise e
              
        flash('Details successfully updated')
        return render_template('home/page-profile.html',
            filename=HeadShot.query.filter_by(user_id=id).first().name,
            full_name='{} {}'.format(user.first_name, user.last_name),
            username=user.username,
            email=user.email,
            phone=user.phone,
            countries=Countries.query.all()
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

def grade_finder(passed, total):
    passed += 1
    total += 1
    
    res = int(passed/total * 100)
    if res > 86:
        return 'A+'
    elif 81 <= res <= 85:
        return 'A-'
    elif 76 <= res <= 80:
        return 'B+'
    elif 69 <= res <= 75:
        return 'B'
    elif 64 <= res <= 68:
        return 'B-'
    elif 59 <= res <= 63:
        return 'C+'
    elif 54 <= res <= 58:
        return 'C'
    elif 49 <= res <= 53:
        return 'C-'
    elif 38 <= res <= 48:
        return 'D'
    else:
        return 'E'