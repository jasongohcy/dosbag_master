from flask import Blueprint, render_template, request,redirect, url_for,flash
import requests
import re
from models.user import User
from models.seller import Seller

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,UserMixin,login_required,logout_user,current_user
from helper import *
from werkzeug.utils import secure_filename



import random

sellHand_blueprint = Blueprint('sellHand',
                            __name__,
                            template_folder='templates')

braintree_blueprint = Blueprint('braintree',
                            __name__,
                            template_folder='templates')                            

@sellHand_blueprint.route('/', methods=['GET'])
def show():            
    return render_template('sellHand/sellHand.html')

@sellHand_blueprint.route('/seller/<fc>', methods=['GET','POST'])
def sellHand_show(fc):
    
    #check if FC exist in DB
    result = Seller.select().where(Seller.choice=="Cabin",Seller.flightcode==fc,Seller.sold==False)
    
    if result:
        
        seller_list = Seller.select().where(Seller.choice=="Cabin",Seller.flightcode==fc,Seller.sold== False, Seller.buyer_id.is_null(True),Seller.sold.is_null(False))   
        
        ranNum = random.randint(0, seller_list.count())        
        ranNum -= 1

        if ranNum < 0:
            ranNum = 0
        else:
            ranNum=ranNum    
        
        return render_template('sellHand/sellHand_market.html', seller=seller_list[0],result=result[ranNum].id)     

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
    seller_id = int(request.args['seller_id'] )
    

    seller = Seller.get(Seller.id == seller_id)
    seller.buyer_id = current_user.id 
    seller.sold = True 
    

    if seller.save():
        flash('Purchase Successful!')
        return redirect(url_for('braintree.new_checkout'))
    else:
        flash('Purchase Failed!')
        return render_template('sellHand/sign_in.html')

    pass


  