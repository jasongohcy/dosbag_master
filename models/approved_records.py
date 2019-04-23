from models.base_model import BaseModel
import peewee as pw
from models.user import User

class ApprovedRecords(BaseModel):
    applied_by  = pw.ForeignKeyField(User),
    approved_by = pw.ForeignKeyField(User)
