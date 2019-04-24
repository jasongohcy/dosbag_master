from flask import Blueprint, render_template, request,redirect, url_for
import requests
import re
from models.seller import Seller
import datetime
from flask_login import login_user,UserMixin,login_required,logout_user,current_user
import os

seller_blueprint = Blueprint('seller',
                            __name__,
                            template_folder='templates')


api = os.environ.get('FLIGHT_API_KEY')

# @seller_blueprint.route('/', methods=['GET'])
# def seller():
#     # now = str(datetime.datetime.now())
    
#     # d = re.search('\d+-\d+-\d+', now)
#     # if d :
#     #     date = d.group(0)
    
#     # t = re.search('\d+:\d+:\d+', now)
#     # if t :
#     #     time = t.group(0)

#     # list_of_sellers = Seller.select().where((Seller.departure_date >= date) & (Seller.sold != True))
#     pass

@seller_blueprint.route('/', methods=['GET' ,'POST'])
def availability():
    flightcode = request.form.get('flightcode')
    time = request.form.get('time')
    date = request.form.get('date')
    now = str(datetime.datetime.now())
    

    if current_user.is_authenticated :

        available = Seller.select().where((Seller.flightcode==flightcode) & (Seller.departure_date==date) & (Seller.departure_time==time) & (Seller.sold ==False) & (Seller.choice=='Luggage') & (Seller.seller_id!=current_user.id))
        d = re.search('\d+-\d+-\d+', now)
        if d :
            date = d.group(0)
        
        t = re.search('\d+:\d+:\d+', now)
        if t :
            time = t.group(0)

        list_of_sellers = Seller.select().where((Seller.departure_date >= date) & (Seller.sold != True) & (Seller.choice=='Luggage') & (Seller.seller_id!=current_user.id))

    else : 

        available = Seller.select().where((Seller.flightcode==flightcode) & (Seller.departure_date==date) & (Seller.departure_time==time) & (Seller.sold ==False) & (Seller.choice=='Luggage') )
        d = re.search('\d+-\d+-\d+', now)
        if d :
            date = d.group(0)
        
        t = re.search('\d+:\d+:\d+', now)
        if t :
            time = t.group(0)

        list_of_sellers = Seller.select().where((Seller.departure_date >= date) & (Seller.sold != True) & (Seller.choice=='Luggage') )
    
    
    return render_template('seller/marketplace.html', available=available,list_of_sellers=list_of_sellers)



@seller_blueprint.route('/sell', methods=['GET'])
@login_required
def sell():
    return render_template('seller/seller.html')

@seller_blueprint.route('/check', methods=['POST'])
def check():
    flightcode= request.form.get('flightcode')
    choice = request.form.get('choice')
    r= requests.get(f"http://aviation-edge.com/v2/public/timetable?key={api}&iataCode=KUL&type=departure")
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
                return render_template('seller/confirm.html',time=time,date=date,flightcodes=flightcodes,departure_time=departure_time,departure_location=departure_location,destination=destination,choice=choice)
    else:
        return render_template('seller/seller.html',error="No Existing Flight Code")
    
    

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
    choice=request.form.get('choice')
    username = current_user.username
    user_id = current_user.id
    seller = Seller.create(choice=choice,username=username, seller_id = user_id, flightcode=flightcode, departure_time=departure_time,departure_date=departure_date,departure_location=departure_location,destination=destination)
    return redirect(url_for('seller.availability'))

@seller_blueprint.route('/buy', methods=['POST'])
def buyer():
    flightcode = request.form.get('flightcode')
    departure_time = request.form.get('departure_time')
    departure_date = request.form.get('departure_date')
    departure_location = request.form.get('departure_location')
    destination = request.form.get('destination')
    username = request.form.get('username')
    seller = Seller.get((Seller.username == username)& (Seller.flightcode==flightcode)& (Seller.departure_time==departure_time) &(Seller.departure_date==departure_date) & (Seller.departure_location==departure_location) & (Seller.destination==destination))
    seller.buyer_id = current_user.id
    seller.sold = True
    seller.amount = 50
    seller.save()
    

    return redirect(url_for('braintree.new_checkout'))


    

