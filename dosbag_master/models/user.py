from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin,current_user
from playhouse.hybrid import hybrid_property
from app import app




class User(BaseModel,UserMixin):
    email = pw.CharField(unique=True,null=False)
    username = pw.CharField(unique=True,null=False)
    password = pw.CharField(unique=False,null=False)
    age = pw.CharField(unique=False,null=False)
    homeaddress = pw.CharField(unique=False,null=False)
    handphone = pw.CharField(unique=False,null=False)
    ic_name = pw.CharField(unique=False,null=False)
    ic_num = pw.CharField(unique=True,null=False)
    nationality = pw.CharField(unique=False,null=False)
    profilepic = pw.CharField(null=True)

    def validate(self):
        duplicate_email = User.get_or_none(User.email == self.email )
        duplicate_username = User.get_or_none(User.username == self.username )
        if duplicate_email and not duplicate_email.id == self.id:
            self.errors.append('Email already exist')
        
        if duplicate_username :
            self.errors.append('Username already exist')
        
        return True
    
    @hybrid_property
    def profilepic_url(self):
        return f"{app.config['S3_LOCATION']}{self.profilepic}"

    @hybrid_property
    def average_rating(self) :
        from models.rate import Rate
        return Rate.select(
            pw.fn.ROUND(((pw.fn.SUM(Rate.score) / (pw.fn.COUNT(Rate.id) + 0.0))), 1).alias("average_score")
            ).where(Rate.user_being_rated_id == self.id)[0].average_score
        