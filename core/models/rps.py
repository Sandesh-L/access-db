from . import *

class RPS(BaseExtModel):
    id = PrimaryKeyField()
    rp_name = CharField(unique=True)
    rp_software_documentation_links = CharField()
    rp_has_individual_software_documentation = BooleanField()
