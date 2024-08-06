from . import *

class RPSoftware(BaseExtModel):
    id = PrimaryKeyField()
    rp_id = ForeignKeyField()
    software_id = ForeignKeyField()
    software_versions = TextField()