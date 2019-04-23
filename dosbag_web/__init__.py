from app import app
from flask import render_template,request
from dosbag_web.blueprints.seller.views import seller_blueprint
from dosbag_web.blueprints.user.views import user_blueprint
from dosbag_web.blueprints.session.views import session_blueprint
from dosbag_web.blueprints.profile.views import profile_blueprint
from dosbag_web.blueprints.braintree.views import braintree_blueprint
from dosbag_web.blueprints.sellHand.views import sellHand_blueprint
import os
from flask_assets import Environment, Bundle
from .util.assets import bundles
import requests


from flask import Blueprint,redirect, url_for,flash
import re
from models.user import User
from models.seller import Seller

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,UserMixin,login_required,logout_user,current_user
from helper import *
from werkzeug.utils import secure_filename

import random



assets = Environment(app)
assets.register(bundles)



app.register_blueprint(seller_blueprint, url_prefix="/seller")
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(session_blueprint, url_prefix="/session")
app.register_blueprint(profile_blueprint, url_prefix="/profile")
app.register_blueprint(braintree_blueprint, url_prefix="/braintree")
app.register_blueprint(sellHand_blueprint, url_prefix="/sellHand")

api = os.getenv('FLIGHT_API_KEY')

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/home")
def homey():
    
    # reply = requests.get('https://api.laminardata.aero/v1/airlines/BAW/flights?user_key=9230b244b3862e197f2ed2c2f98af1e1')
    # x = xmltodict.parse(reply._content)
    # second = x['message:flightMessage']['fx:Flight'][0]['fx:aircraftDescription']
    r= requests.get(f"http://aviation-edge.com/v2/public/timetable?key={api}&iataCode=KUL&type=departure")
    reply = r.json()
    # name = []
    # for i in reply :
    #     if i.airline.name != n :
    #         name.append(i.airline.name)
    # r = requests.get('https://api.flightstats.com/flex/schedules/rest/v1/json/from/KUL/to/SIN/departing/2019/04/14?appId=7438e45d&appKey=fbfceee0e0d57d6f5baf703ad54e3003')
    # reply = r.json()
    # listy = reply['scheduledFlights']
    return render_template('home.html',reply=reply)


@app.route("/")
def home() :
    return render_template('homepage2.html')


@sellHand_blueprint.route('/', methods=['GET'])
def show():            
    return render_template('sellHand/sellHand.html')

@sellHand_blueprint.route('/seller/<fc>', methods=['GET'])
def sellHand_show(fc):
    
    #check if FC exist in DB
    
    result = Seller.select().where(Seller.choice=="Cabin",Seller.flightcode==fc)
    
    if result:

        seller_list = Seller.select().where(Seller.choice=="Cabin",Seller.flightcode==fc,Seller.sold== False, Seller.buyer_id.is_null(True),Seller.sold.is_null(False))   
        
        ranNum = random.randint(0, seller_list.count())        
        ranNum -= 1

        if ranNum < 0:
            ranNum = 0
        else:
            ranNum=ranNum    

        return render_template('sellHand/sellHand_market.html', seller=seller_list[ranNum])     

    else:
        return render_template('sellHand/sellHand.html')

@sellHand_blueprint.route('/location', methods=['GET'])
def checkLocation():
    
    latitude = float(request.args['lat'])
    longitude = float(request.args['lng'])
    fc = request.args['fc']

    latitude = float("{0:.4f}".format(latitude))
    longitude = float("{0:.4f}".format(longitude))

    if (3.0000 < latitude < 3.2000) and (101.5000 < longitude < 101.7000):    
        return redirect(url_for("sellHand.sellHand_show",fc=fc))
    else:
        return render_template('sellHand/sellHand/test.html')

@sellHand_blueprint.route('/confirmBuy', methods=['GET'])
def confirmBuy():

    seller_id = request.args['seller_id']  
    seller = Seller.get(Seller.seller_id == seller_id)
    seller.buyer_id = current_user.id 
    seller.sold = True 
    
    if seller.save():
        flash('Purchase Successful!')
        return redirect(url_for('braintree.new_checkout'))
    else:
        flash('Purchase Failed!')
        return render_template('sellHand/sign_in.html')

        