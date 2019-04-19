from flask import Blueprint, render_template, request,redirect, url_for
import requests
import re
from models.user import User
from models.seller import Seller
from models.rate import Rate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,UserMixin,login_required,logout_user,current_user
from helper import *
from werkzeug.utils import secure_filename

profile_blueprint = Blueprint('profile',
                            __name__,
                            template_folder='templates')

@profile_blueprint.route('/', methods=['GET'])
@login_required
def profile():
    pic = User.get(User.id == current_user.id).profilepic_url
    purchase = Seller.select().where(Seller.buyer_id == current_user.id)
    rated = Rate.select().where(Rate.rater_id == current_user.id)
    rated_ids = [r.user_being_rated_id.id for r in rated]
    everyone = User.select()
    # score = []
    # for r in rated :
    #     sum_score = Rate.select(fn.SUM('score')).where(Rate.user_being_rated_id == r.user_being_rated_id)
    #     total_records = raters.count()
    #     final_rating = sum_score/total_records
    #     score.append(final_rating)


    
    return render_template('profile/profile.html',pic=pic,purchase=purchase,rated_ids=rated_ids)

@profile_blueprint.route('/pic', methods=['POST'])
def profilepic():
    if "user_file" not in request.files:
        return "No user_file key in request.files"
    file = request.files["user_file"]
    if file.filename == "":
        return "Please select a file"
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file, app.config["S3_BUCKET"])
        q = (User.update({User.profilepic: file.filename}).where(User.id == current_user.id))
        q.execute()
        return redirect(url_for('profile.profile'))
    else:
        return redirect(url_for('profile.profile'))



@profile_blueprint.route('/user/<id>', methods=['GET'])
def userprofile(id):
    int_id = int(id)
    user = User.get(User.id == int_id)
    username = user.username
    ic_name = user.ic_name
    handphone = user.handphone
    profilepic =user.profilepic
    purchase = Seller.select().where(Seller.buyer_id == int_id)
    return render_template('profile/userprofile.html',int_id=int_id,username=username,ic_name=ic_name,handphone=handphone,profilepic=profilepic,purchase=purchase)
    
    
# @profile_blueprint.route('/score', methods=['POST'])
# def score() :
#     score = request.form.get('score')
#     current_id = request.form.get('current')
#     return redirect(url_for('profile.userprofile',id = current_id ))



@profile_blueprint.route('/edit', methods=['GET'])
@login_required
def edit():
    return render_template('profile/editprofile.html')

@profile_blueprint.route('/editprocess', methods=['POST'])
@login_required
def editprofile():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    new_password = request.form.get('new_password')
    new_hashed_password = generate_password_hash(new_password)
    if check_password_hash(current_user.password, password) : 
        if re.search(".{6,}",new_password) and re.search("[a-z]",new_password) and re.search("[A-Z]",new_password) and re.search ("\W",new_password):
            user = User.get(User.username == current_user.username) 
            user.username = username
            user.email = email
            user.password =new_hashed_password
            if user.save():    
                return redirect(url_for('profile.profile'))
            else :
                return render_template("profile/editprofile.html", errors=user.errors)
        else :
            return render_template('profile/editprofile.html', passworderror="Password must have at least 6 characters,contains symbols,small and capital letters.")
    else:
        return render_template('profile/editprofile.html', old_password_error = "The Old Password You Keyed In Does Not Match The Current Password You Have")


@profile_blueprint.route('/rate', methods=['POST'])
@login_required
def rate():
    user_being_rated_id = request.form.get('user_being_rated_id')
    rate = int(request.form.get('rate'))
    rating = Rate.create(user_being_rated_id=user_being_rated_id,rater_id= current_user.id,score=rate)
    return redirect(url_for('profile.profile'))