from ..models import *
from models.software import Software
from models.rps import RPS
from models.rpSoftware import RPSoftware
import pandas as pd
from ...parseSpiderOutput import parse_spider_output

def get_software_from_name(software_name):
    pass



def create_rp_software_records(parsed_spider_output):
    
    rps = parse_spider_output.key()

    for rp in rps:
        software, versions = parse_spider_output[rp]
        


    # {rp: [(softare, version), (software, version), (software, version)]}
    #
    # {rp_id:rp_id, software_id:software_id, version:version}




    pass    

@db.connection_context()
def create_rp_software_table():
    db.drop_tables([RPSoftware])
    db.create_tables([RPSoftware])

@db.connection_context()
def update_rp_software_table(rp_software_records):
    pass


create_rp_software_table()
parsed_spider_output = parse_spider_output()
rp_software_records = create_rp_software_records(parsed_spider_output)

print(rp_software_records)
update_rp_software_table(rp_software_records)


rp_software = RPSoftware.select()

for rp_s in rp_software:
    print(f"software: {rp_s.rp_id.rp_name}, \
          desc: {rp_s.software_id.software_name}, \
          web_p: {rp_s.software_versions},"
          )





if __name__ =="__main__":#
    pass