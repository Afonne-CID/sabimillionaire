import uuid
import requests
from flask import jsonify, render_template, request, flash
from flask_login import login_required, current_user
from app.transaction import blueprint
from app.home.routes import paginate_rtr
from ..models import *
from app.home.routes import get_headshot


@blueprint.route('/fund-account', methods=['GET', 'POST'])
@login_required
def account_fund():
    ''''''
    id = current_user.get_id()
    headshot = get_headshot()

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

        if amount <= 0:
            flash('Invalid amount')

        deposit = Deposit(status=status,
                        reference=response['data']['reference'],
                        created_at=response['data']['created_at'],
                        paid_at=response['data']['paid_at'],
                        currency=response['data']['currency'],
                        payment_option=response['data']['channel'],
                        user_id=id,
                        amount=amount,
                )        

        if status == 'success':
            account = Account.query.filter_by(user_id=id).first()
            account.wallet_balance += amount

        db.session.add(deposit)
        db.session.commit()

    deposits = Deposit.query.filter_by(user_id=id).all()

    paginate = paginate_rtr()
    start = paginate['start']
    end = paginate['end']
    page = paginate['page']
    count = paginate['count']
    d_len = len(deposits)
    total_pages = d_len if ((d_len / count) - (int(d_len / count))) == 0 else d_len + count


    return render_template('transaction/make-payment.html',
                            segment='account-fund',
                            filename=headshot.name,
                            payments=deposits[start:end],
                            total_pages=total_pages,
                            page=page,
                            end=end,
                            count=count
    )


@blueprint.route('/withdraw-fund', methods=['GET', 'POST'])
@login_required
def account_withdraw():
    ''''''
    id = current_user.get_id()
    headshot = get_headshot()
    withdrawals = Withdraw.query.filter_by(user_id=id).all()
    min_withdraw = Admin.query.first().min_withdraw
    wallet_balance = Account.query.filter_by(user_id=id).first().wallet_balance

    paginate = paginate_rtr()
    start = paginate['start']
    end = paginate['end']
    page = paginate['page']
    count = paginate['count']
    d_len = len(withdrawals)
    total_pages = d_len if ((d_len / count) - (int(d_len / count))) == 0 else d_len + count

    if request.method == 'POST':

        user = User.query.get(id)
        details = request.form
        print(details)

        first_name = user.first_name
        last_name = user.last_name
        amount = float(details.get('amount'))
        
        if amount > wallet_balance:
            flash('Insufficient balance')
        if amount <= 0:
            flash('Invalid amount')

        if (first_name == details.get('first-name') and
            last_name == details.get('last-name')):

            bank_name = details.get('bank-name')
            account_number = float(details.get('account-number'))
            amount = float(details.get('amount'))

            if bank_name and account_number:
                withdraw = Withdraw(**request.form)

                db.session.add(withdraw)
                db.session.commit()

                flash('Withdraw request has been submitted successfully')
            else:
                flash('All details are required')
        else:
            flash('Widthdrawal details and profile details must match.')

    return render_template('transaction/withdraw.html',
                            segment='account-withdraw',
                            filename=headshot.name,
                            withdrawals=withdrawals[start:end],
                            total_pages=total_pages,
                            page=page,
                            end=end,
                            count=count,
                            min_withdraw=min_withdraw,
                            wallet_balance=wallet_balance
            )

@blueprint.route('/buy-slots', methods=['POST'])
def buy_slots():
    ''''''
    id = current_user.get_id()
    headshot = get_headshot()
    withdrawals = Withdraw.query.filter_by(user_id=id).all()
    min_withdraw = Admin.query.first().min_withdraw
    account = Account.query.filter_by(user_id=id).first()
    wallet_balance = account.wallet_balance

    paginate = paginate_rtr()
    start = paginate['start']
    end = paginate['end']
    page = paginate['page']
    count = paginate['count']
    d_len = len(withdrawals)
    total_pages = d_len if ((d_len / count) - (int(d_len / count))) == 0 else d_len + count

    deposits = Deposit.query.filter_by(user_id=id).all()
    cost_per_slot = Admin.query.first().cost_per_slot


    if 'buy-slots' in request.form:
        ''''''

        if wallet_balance < cost_per_slot:
            flash('You need at least {} to get a game slot'.format(cost_per_slot))
        else:
            qty = int(request.form['qty'])

            try:
                account.wallet_balance -= (qty * 200)
                account.slots += qty * 2
                db.session.commit()

            except:
                db.session.rollback()

            flash('Action was successful')

    return render_template('home/index.html',
                        segment='index',
                        wallet=account.wallet_balance,
                        total_correct=account.total_correct,
                        total_failed=account.total_failed,
                        total_attempted=account.total_attempted,
                        slots=account.slots,
                        coin_balance=account.coin_balance,
                        filename=headshot.name,
                        payments=deposits[start:end],
                        total_pages=total_pages,
                        page=page,
                        end=end,
                        coins=account.coin_balance,
                        count=count,
            )


def payment_reference():
    ''''''
    val = str(uuid.uuid4()).split('-')
    
    return val[-1] + val[1]