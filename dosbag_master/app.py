import os
import config
from flask import Flask
from models.base_model import db
from flask_login import LoginManager, login_user
from flask_wtf.csrf import CSRFProtect

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'dosbag_web')

app = Flask('dosbag', root_path=web_dir)
login_manager = LoginManager()
login_manager.init_app(app)
csrf = CSRFProtect(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.get_by_id(int(user_id))


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
