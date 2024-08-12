from ..models import edit_db
from ..models.software import Software
from ..models.rps import RPS
from ..models.rpSoftware import RPSoftware
from ..parseSpiderOutput import parse_spider_output
import pandas as pd

rp_with_individual_software_page = ["Anvil", "Bridges-2", "DARWIN"]

# Hard-coded links to RP-specific Software Documentation
RP_URLS = {
    'Aces':'https://hprc.tamu.edu/software/aces/',
    'Anvil': 'https://www.rcac.purdue.edu/software/',
    'Bridges-2': 'https://www.psc.edu/resources/software/',
    'DARWIN': 'https://docs.hpc.udel.edu/software/',
    'Delta': 'https://docs.ncsa.illinois.edu/systems/delta/en/latest/user_guide/software.html',
    'Expanse':'https://www.sdsc.edu/support/user_guides/expanse.html#modules',
    'Faster':'https://hprc.tamu.edu/software/faster/',
    'Jetstream2':'',
    'Kyric':'',
    'Ookami':'https://www.stonybrook.edu/commcms/ookami/support/faq/software_on_ookami',
    'Stampede3':'https://tacc.utexas.edu/use-tacc/software-list/',
    'Ranch':'https://tacc.utexas.edu/use-tacc/software-list/',
    'OSG':'',
    'OSN':''
}

software_types = {
    "anvil": {
        "igenomes": "knowledge"
    }
}

#################################################################################
#   create_rp_software_records                                                  #
#       Creates 'records' of data to add to the RPSoftware table. Software, RP, #
#       and software_versions are obtained from module spider data              #
#       (parsed_spider_output). rp documentation, individual documentation and  #
#       software documentation are obtained from the global variables in this   #
#       file.                                                                   #
#   Args:                                                                       #
#       parsed_spider_output {Dict}: A dictionary with rp name as the key       #
#           and a tuple of software and versions as the values (returned from   #
#           parse_spider_output function)                                       #
#                                                                               #
#    Return:                                                                    #
#        records {list{dict}}: list of records to be added to the RPS table.    #
#                The keys of the dict are columns in the table                  #
#################################################################################
# TODO: NEED TO ADD SUPPORT FOR rp_software_types
def create_rp_software_table_records(parsed_spider_output):
    
    rp_software_records = []

    rps = parsed_spider_output.keys()
    for rp in rps:

        rp_id = RPS.get(RPS.rp_name == rp)
        # rp_software_types = software_types[rp]

        for software, versions in parsed_spider_output[rp]:
            software_id = Software.get(Software.software_name == software)
            rp_software_records.append({
                "rp_id": rp_id,
                "software_id": software_id,
                "software_versions": versions,
                "rp_software_documentation": RP_URLS[rp] if rp in RP_URLS else "",
                "rp_has_individual_software_documentation": 1 if rp in rp_with_individual_software_page else 0,
                # "rp_software_type": rp_software_types[]
            })

    return rp_software_records


#################################################################################
#   update_rp_software_table                                                    #
#       Adds data to the RPSoftware table based on provided rp_software_records.#
#       In cases where the rp_name and software_name combination is already in  #
#       the table, it updates the data for that row.                            #
#   Args:                                                                       #
#       rp_software_records {list{dict}}: A list of dict items where each key   #
#           in the dict is a column in the RPS table (returned from             #
#           create_rp_software_table_records())                                 #
#################################################################################
@edit_db.connection_context()
def update_rp_software_table(rp_software_records):

    with edit_db.atomic():
        RPSoftware.insert_many(rp_software_records).on_conflict(
            conflict_target=[RPSoftware.software_id, RPSoftware.rp_id],  # If there is a conflict on the `Unique` constraint of rp_id and software_id
            preserve=[RPSoftware.software_versions, 
                    RPSoftware.rp_software_documentation, 
                    RPSoftware.rp_has_individual_software_documentation, 
                    ]   # Update the existing rp entry using the incomming (new) data
        ).execute()



if __name__ =="__main__":
    pass