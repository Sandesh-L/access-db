from models import db
from models.rps import RPS




rp_names = ["Aces","Anvil","Bridges-2","DARWIN","Delta","Expanse","Faster","Jetstream2","Kyric","Ookami","Stampede3","Ranch","OSG","OSN"]

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


#################################################################################
#   generate_rp_table_records                                                   #
#       Generates a list of dicts where each dict represents a row in the RPS   #
#       table. Each key in the dict corrosponds to a column in the RPS table.   #
#                                                                               #
#    Return:                                                                    #
#        records {list{dict}}: list of records to be added to the RPS table     #
#################################################################################
def generate_rp_table_records():

    records = []
    for rp_name in rp_names:
        record = {"rp_name":rp_name,
                  "rp_software_documentation_links":RP_URLS[rp_name],
                  "rp_has_individual_software_documentation": 1 if rp_name in rp_with_individual_software_page else 0}
        
        records.append(record)

    return records



#################################################################################
#   update_rp_table                                                             #
#       Adds data to the RPS table based on provided rp_records. In cases where #
#       the rp_name is already in the table, it updates the data for that row   #
#   Args:                                                                       #
#       rp_recods {list{dict}}: A list of dict items where each key in the dict #
#       is a column in the RPS table (returned from generate_rp_table_records())#
#   Return:                                                                     #
#        records {list{dict}}: list of records to be added to the RPS table     #
#################################################################################
@db.connection_context()
def update_rp_table(rp_records):
    
    RPS.insert_many(rp_records).on_conflict(
        conflict_target=[RPS.rp_name],  # If there is a conflict on the `Unique` constraint of rp_name
        preserve=[RPS.rp_software_documentation_links, RPS.rp_has_individual_software_documentation],    # Update the existing rp entry using the incomming (new) data
    ).execute()


# TODO: should be moved away from this file
# Connect to the db and create tables
@db.connection_context() # opens a db connectionon function call, conn is closed on function return
def setup_db():
    db.drop_tables([RPS])
    db.create_tables([RPS])



setup_db()
rp_records = generate_rp_table_records()
update_rp_table(rp_records)

rps = RPS.select()
for rp in rps:
    print(f'rp: {rp.rp_name}, links: {rp.rp_software_documentation_links}, rp_has_individual_sftw_docs: {rp.rp_has_individual_software_documentation}')


if __name__ =="__main__":
    pass