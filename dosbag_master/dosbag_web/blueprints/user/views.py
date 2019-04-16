from flask import Blueprint, render_template, request,redirect, url_for
import requests
import re
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,UserMixin,login_required,logout_user,current_user


user_blueprint = Blueprint('user',
                            __name__,
                            template_folder='templates')

@user_blueprint.route('/', methods=['GET'])
def signup():
    return render_template('user/Signup.html')

@user_blueprint.route('/create', methods=['POST'])
def create():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    age = request.form.get('age')
    homeaddress = request.form.get('homeaddress')
    handphone = request.form.get('handphone')
    ic_name = request.form.get('ic_name')
    ic_num = request.form.get('ic_num')
    nationality = request.form.get('nationality')
    hashed_password = generate_password_hash(password)
    if re.search(".{6,}",password) and re.search("[a-z]",password) and re.search("[A-Z]",password) and re.search ("\W",password):
        q = User(email=email, password=hashed_password, username=username,age=age,homeaddress=homeaddress,handphone=handphone,ic_name=ic_name,ic_num=ic_num,nationality=nationality)
        if q.save():
            return redirect(url_for('seller.seller'))
        else :
            return render_template("user/SignUp.html", errors=q.errors)
    else :
        return render_template("user/new.html", passworderror="Password must have at least 6 characters,contains symbols,small and capital letters.")
    return redirect(url_for("user.nothing"))

@user_blueprint.route('/nothing', methods=['GET'])
def nothing():
    return "Yay!"