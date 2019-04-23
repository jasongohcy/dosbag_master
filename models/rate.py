from models.base_model import BaseModel
import peewee as pw
from models.user import User

class Rate(BaseModel):
    user_being_rated_id = pw.ForeignKeyField(User, backref='sellers',null=False)
    rater_id = pw.ForeignKeyField(User, backref='raters',null=False)
    score = pw.IntegerField()
    rated = pw.BooleanField(default=True)
