from . import *

class RPS(BaseExtModel):
    id = PrimaryKeyField()
    rp_name = CaseInsensitiveField(unique=True, null=False)
