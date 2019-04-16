from models.base_model import BaseModel
import peewee as pw

class Product(BaseModel):
    product_name = pw.CharField(),
    product_price = pw.IntegerField(),
     


