from flask import Blueprint, render_template, request,redirect, url_for,flash, Flask,session
import re
from flask_login import login_user,login_required,logout_user,current_user
from app import *
import braintree
import os
from os.path import join, dirname
from dotenv import load_dotenv
from gateway import generate_client_token, transact, find_transaction


braintree_blueprint = Blueprint('braintree',
                            __name__,
                            template_folder='templates')

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app.secret_key = os.environ.get('APP_SECRET_KEY')


TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]


@braintree_blueprint.route('/', methods=['GET'])
def new_checkout():
    client_token = generate_client_token()
    return render_template('braintree/new.html', client_token=client_token)




@braintree_blueprint.route('/checkouts/result', methods=['POST'])
def create_checkout():
    result = transact({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })
    amount = int(request.form.get('amount'))


    if result.is_success or result.transaction:
        
        # message = Mail(
        #     from_email='chunghanwong99@gmail.com',
        #     to_emails= current_email,
        #     subject='Sending with SendGrid is Fun',
        #     html_content=f"The amount of money transacted to NEXT Academy is $ {amount}. Please call your bank your if you are not aware of this payment. Have a great day!")
        # try:
        #     sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        #     response = sg.send(message)
        #     print(response.status_code)
        #     print(response.body)
        #     print(response.headers)
        # except Exception as e:
        #     print(e.message)
        return redirect(url_for('braintree.show_checkout',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('braintree.new_checkout'))




@braintree_blueprint.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    transaction = find_transaction(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('braintree/show.html', transaction=transaction, result=result)