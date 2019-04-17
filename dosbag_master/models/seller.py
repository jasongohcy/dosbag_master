from models.base_model import BaseModel
import peewee as pw
from models.user import User

class Seller(BaseModel):
    username = pw.CharField(unique=False,null=True)
    seller_id = pw.ForeignKeyField(User, backref='sellers',null=True)
    buyer_id = pw.ForeignKeyField(User, backref='buyers',null=True)
    flightcode = pw.CharField()
    departure_time = pw.CharField()
    departure_date= pw.CharField()
    departure_location = pw.CharField()
    destination= pw.CharField()
    sold = pw.BooleanField(default=False)
    amount = pw.DecimalField(null=True)
    # transaction_completed = pw.BooleanField(default=False)

