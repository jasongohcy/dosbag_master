from models.base_model import BaseModel
import peewee as pw

class param(BaseModel):
    weight = pw.IntegerField(),
    price  = pw.IntegerField()
