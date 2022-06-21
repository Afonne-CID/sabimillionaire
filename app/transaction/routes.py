import uuid
import requests
from flask import jsonify, render_template, request, flash
from flask_login import login_required, current_user
from app.transaction import blueprint
from app.home.routes import paginate_rtr
from ..models import *


@blueprint.route('/fund-account', methods=['GET', 'POST'])
@login_required
def account_fund():
    ''''''
    id = current_user.get_id()
    headshot = HeadShot.query.filter_by(user_id=id).first()

    ref = request.args.get('reference')
    status = 'failed'
    amount = 0

    if ref:
        url = 'https://api.paystack.co/transaction/verify/{}'.format(ref)
        token = 'sk_test_c28bf021fe3c0afafc6414ac3ef4cb9bcaaa3b03'

        req = requests.get(url,
                headers={'Content-Type':'application/json',
                        'Authorization': 'Bearer {}'.format(token)})

        response = req.json()
        status = response['data']['status']
        amount = response['data']['amount'] / 100

        deposit = Deposit(status=status,
                        reference=response['data']['reference'],
                        created_at=response['data']['created_at'],
                        paid_at=response['data']['paid_at'],
                        currency=response['data']['currency'],
                        payment_option=response['data']['channel'],
                        user_id=id,
                        amount=amount,
                )        

        db.session.add(deposit)
        db.session.commit()

    deposits = Deposit.query.filter_by(user_id=id).all()

    paginate = paginate_rtr()
    start = paginate['start']
    end = paginate['end']
    page = paginate['page']
    count = paginate['count']

    return render_template('transaction/make-payment.html',
                            filename=headshot.name,
                            payments=deposits[start:end],
                            total_pages=len(deposits),
                            page=page,
                            end=end,
                            count=count
    )


@blueprint.route('/withdraw-fund', methods=['GET', 'POST'])
@login_required
def account_withdraw():
    ''''''
    id = current_user.get_id()
    headshot = HeadShot.query.filter_by(user_id=id).first()

    withdrawals = Withdraw.query.filter_by(user_id=id).all()

    paginate = paginate_rtr()
    start = paginate['start']
    end = paginate['end']
    page = paginate['page']
    count = paginate['count']

    return render_template('transaction/withdraw.html',
                            filename=headshot.name,
                            withdrawals=withdrawals[start:end],
                            total_pages=len(withdrawals),
                            page=page,
                            end=end,
                            count=count
            )