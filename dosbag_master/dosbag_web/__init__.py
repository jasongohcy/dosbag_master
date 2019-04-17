from app import app
from flask import render_template,request
from dosbag_web.blueprints.seller.views import seller_blueprint
from dosbag_web.blueprints.user.views import user_blueprint
from dosbag_web.blueprints.session.views import session_blueprint
from dosbag_web.blueprints.profile.views import profile_blueprint
from dosbag_web.blueprints.braintree.views import braintree_blueprint

from flask_assets import Environment, Bundle
from .util.assets import bundles
import requests


assets = Environment(app)
assets.register(bundles)

app.register_blueprint(seller_blueprint, url_prefix="/seller")
app.register_blueprint(user_blueprint, url_prefix="/user")
app.register_blueprint(session_blueprint, url_prefix="/session")
app.register_blueprint(profile_blueprint, url_prefix="/profile")
app.register_blueprint(braintree_blueprint, url_prefix="/braintree")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/home")
def homey():
    # reply = requests.get('https://api.laminardata.aero/v1/airlines/BAW/flights?user_key=9230b244b3862e197f2ed2c2f98af1e1')
    # x = xmltodict.parse(reply._content)
    # second = x['message:flightMessage']['fx:Flight'][0]['fx:aircraftDescription']
    r= requests.get('http://aviation-edge.com/v2/public/timetable?key=342cbb-b8d23f&iataCode=KUL&type=departure')
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
    return render_template('Homepage.html')