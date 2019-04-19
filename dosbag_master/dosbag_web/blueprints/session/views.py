from flask import Blueprint, render_template, request,redirect, url_for,session
import requests
import re
from models.seller import Seller
from models.user import User
import datetime
from flask_login import login_user,UserMixin,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash

session_blueprint = Blueprint('session',
                            __name__,
                            template_folder='templates')

@session_blueprint.route('/', methods=['GET'])
def login():
    return render_template('session/Login.html')

@session_blueprint.route('/', methods=['POST'])
def check():
    email = request.form.get('email')
    password = request.form.get('password')
    email_from_database = User.select()
    for e in email_from_database :
        if email == e.email :
            if check_password_hash(e.password, password) :
                login_user(e)
                return redirect(url_for('seller.seller'))
            else:
                return render_template('session/Login.html', passworderror = "Wrong Password")
    return render_template('sessions/Login.html', emailerror="Wrong Email")


@session_blueprint.route('/logout', methods=["POST","GET"])
def logout():
    logout_user()
    return redirect('/')
