from flask import Blueprint, render_template, request,redirect, url_for
import requests
import re
from models.seller import Seller
import datetime
from flask_login import login_user,UserMixin,login_required,logout_user,current_user

seller_blueprint = Blueprint('seller',
                            __name__,
                            template_folder='templates')


@seller_blueprint.route('/sell', methods=['GET'])
def sell():
    return render_template('seller/seller.html')

@seller_blueprint.route('/', methods=['GET'])
def seller():
    now = str(datetime.datetime.now())

    d = re.search('\d+-\d+-\d+', now)
    if d :
        date = d.group(0)
    
    t = re.search('\d+:\d+:\d+', now)
    if t :
        time = t.group(0)

    list_of_sellers = Seller.select().where((Seller.departure_date >= date) & (Seller.sold != True))
    return render_template('seller/marketplace.html',list_of_sellers=list_of_sellers)


@seller_blueprint.route('/check', methods=['POST'])
def check():
    flightcode= request.form.get('flightcode')
    r= requests.get(' http://aviation-edge.com/v2/public/timetable?key=342cbb-b8d23f&iataCode=KUL&type=departure')
    reply = r.json()
    code = [i['flight']['iataNumber'] for i in reply]

    if flightcode in code:
        for i in reply :
            if i['flight']['iataNumber'] == flightcode :
                flightcodes = flightcode
                departure_time = i['departure']['scheduledTime']
                d = re.search('\d+-\d+-\d+', departure_time)
                if d :
                    date = d.group(0)
                t = re.search('\d+:\d+:\d+', departure_time)
                if t :
                    time = t.group(0)
                departure_location = i['departure']['iataCode']
                destination = i['arrival']['iataCode']
                return render_template('seller/confirm.html',time=time,date=date,flightcodes=flightcodes,departure_time=departure_time,departure_location=departure_location,destination=destination)
    else:
        return render_template('seller/marketplace.html',error="No Existing Flight Code")
    
    

@seller_blueprint.route('/confirm', methods=['GET'])
def confirm():
    return render_template('seller/confirm.html')

@seller_blueprint.route('/post', methods=['POST'])
def post():
    flightcode = request.form.get('flightcode')
    departure_time = request.form.get('departure_time')
    departure_date = request.form.get('departure_date')
    departure_location = request.form.get('departure_location')
    destination = request.form.get('destination')
    username = current_user.username
    user_id = current_user.id
    seller = Seller.create(username=username, seller_id = user_id, flightcode=flightcode, departure_time=departure_time,departure_date=departure_date,departure_location=departure_location,destination=destination)
    return redirect(url_for('seller.seller'))

@seller_blueprint.route('/buy', methods=['POST'])
def buyer():
    # flightcode = request.form.get('flightcode')
    # departure_time = request.form.get('departure_time')
    # departure_date = request.form.get('departure_date')
    # departure_location = request.form.get('departure_location')
    # destination = request.form.get('destination')
    username = request.form.get('username')
    seller = Seller.get(Seller.username == username)
    seller.buyer_id = current_user.id
    seller.sold = True
    seller.amount = 50
    seller.save()
    # seller = (Seller.update({}))
    return redirect(url_for('braintree.new_checkout'))


    

