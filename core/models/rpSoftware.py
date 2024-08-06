from . import *
from .rps import RPS
# from .rps import RPS
from .software import Software
class RPSoftware(BaseExtModel):

    id = PrimaryKeyField()
    rp_id = ForeignKeyField(RPS)
    software_id = ForeignKeyField(Software)
    software_versions = TextField()