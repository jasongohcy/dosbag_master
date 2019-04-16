from flask import Blueprint, render_template, request,redirect, url_for
import requests
import re
from models.user import User
from models.seller import Seller
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,UserMixin,login_required,logout_user,current_user
from helper import *
from werkzeug.utils import secure_filename

profile_blueprint = Blueprint('profile',
                            __name__,
                            template_folder='templates')

@profile_blueprint.route('/', methods=['GET'])
def profile():
    purchase = Seller.select().where(Seller.buyer_id == current_user.id)
    # pic = User.get(User.id == current_user.id)
    
    return render_template('profile/profile.html',purchase=purchase)

@profile_blueprint.route('/pic', methods=['POST'])
def profilepic():
    if "user_file" not in request.files:
        return "No user_file key in request.files"
    file = request.files["user_file"]
    if file.filename == "":
        return "Please select a file"
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        # output = upload_file_to_s3(file, app.config["S3_BUCKET"])
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
    
    
@profile_blueprint.route('/score', methods=['POST'])
def score() :
    score = request.form.get('score')
    current_id = request.form.get('current')
    return redirect(url_for('profile.userprofile',id = current_id ))