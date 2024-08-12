from . import *
from datetime import datetime

class API(BaseExtModel):
    id = PrimaryKeyField()
    organization = CharField()
    api_key = TextField(unique=True)
    date_generated = DateField(default=datetime.now)
