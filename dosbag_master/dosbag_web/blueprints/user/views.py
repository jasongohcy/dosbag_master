from flask import Blueprint, render_template, request,redirect, url_for
import requests
import re
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,UserMixin,login_required,logout_user,current_user
from clarifai import rest
from clarifai.rest import ClarifaiApp,Image as ClImage
import os

app = ClarifaiApp(api_key=os.environ["CLARIFAI_API_KEY"])

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
    homeaddress2 = request.form.get('homeaddress2')
    handphone = request.form.get('handphone')
    ic_name = request.form.get('ic_name')
    ic_num = request.form.get('ic_num')
    nationality = request.form.get('nationality')
    hashed_password = generate_password_hash(password)
    user_database = User.select()
    if re.search(".{6,}",password) and re.search("[a-z]",password) and re.search("[A-Z]",password) and re.search ("\W",password):
        for u in user_database :
            if username == u.username :
                return render_template("user/Signup.html", usernameerror = "Username already exists")
            elif email == u.email :
                return render_template("user/Signup.html",emailerror = "Email already exists")
        return render_template("user/clarifai.html",homeaddress2 = homeaddress2, email=email, password=hashed_password, username=username,age=age,homeaddress=homeaddress,handphone=handphone,ic_name=ic_name,ic_num=ic_num,nationality=nationality )
    else :
        return render_template("user/Signup.html", passworderror="Password must have at least 6 characters,contains symbols,small and capital letters.")
    


@user_blueprint.route('/clarifai', methods=['GET'])
def imageURL():
    
    return render_template('user/clarifai.html')


@user_blueprint.route('/clarifai/tags', methods=['POST'])
def tags():
    # upload by url

    imageURL = request.form.get('imageURL')
    model = app.public_models.general_model
    result = model.predict_by_url(url=imageURL)
    all_people_text = []
    response_data = result['outputs'][0]['data']['concepts']
    all_people_text = [data for data in response_data if (data["name"] == "people" or data["name"] == "text") and data["value"] > 0.8]
    if len(all_people_text) == 2:
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        age = request.form.get('age')
        homeaddress = request.form.get('homeaddress')
        homeaddress2 = request.form.get('homeaddress2')
        handphone = request.form.get('handphone')
        ic_name = request.form.get('ic_name')
        ic_num = request.form.get('ic_num')
        nationality = request.form.get('nationality')
        
        q = User(email=email, password=password, username=username,age=age,homeaddress=homeaddress,homeaddress2=homeaddress2,handphone=handphone,ic_name=ic_name,ic_num=ic_num,nationality=nationality)
        if q.save():
            user = User.get(User.username == username)
            login_user(user)
            return redirect(url_for('seller.availability'))
        else :
            return render_template("user/SignUp.html", errors=q.errors)
    return render_template('user/clarifai.html', error = "The Picture Sent Does Not Contain An IC")


@user_blueprint.route('/clarifai/tag-file', methods=['POST'])
def localhost():
    # upload by local host
    file = request.files['local']
    model = app.public_models.general_model
    result2 = model.predict_by_bytes(file.stream.read())


    all_people_text2 = []
    response_data = result2['outputs'][0]['data']['concepts']
    all_people_text2 = [data for data in response_data if (data["name"] == "people" or data["name"] == "text") and data["value"] > 0.8]
    if len(all_people_text2) == 2:
        
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        age = request.form.get('age')
        homeaddress = request.form.get('homeaddress')
        handphone = request.form.get('handphone')
        ic_name = request.form.get('ic_name')
        ic_num = request.form.get('ic_num')
        nationality = request.form.get('nationality')
        homeaddress2 = request.form.get('homeaddress2')
        q = User(email=email, password=password, username=username,age=age,homeaddress=homeaddress,homeaddress2=homeaddress2,handphone=handphone,ic_name=ic_name,ic_num=ic_num,nationality=nationality)
        
        if q.save():
            user = User.get(User.username == username)
            login_user(user)
            return redirect(url_for('seller.availability'))
        else :
            return render_template("user/SignUp.html", errors=q.errors)
    return render_template('user/clarifai.html',error = "The Picture Sent Does Not Contain An IC")