from . import *

class AISoftwareInfo(BaseExtModel):
    id = PrimaryKeyField()
    software_id = ForeignKeyField()
    ai_description = TextField()
    ai_example_use = TextField()