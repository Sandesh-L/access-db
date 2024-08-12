from ..models import edit_db
from ..models.rps import RPS

rp_names = ["Aces","Anvil","Bridges-2","DARWIN","Delta","Expanse","Faster","Jetstream2","Kyric","Ookami","Stampede3","Ranch","OSG","OSN"]


#################################################################################
#   create_rp_table_records                                                     #
#       creates a list of dicts where each dict represents a row in the RPS     #
#       table. Each key in the dict corrosponds to a column in the RPS table.   #
#                                                                               #
#    Return:                                                                    #
#        records {list{dict}}: list of records to be added to the RPS table     #
#################################################################################
def create_rp_table_records():

    records = []
    for rp_name in rp_names:
        record = {"rp_name":rp_name}
        records.append(record)

    return records


#####################################################################################
#   update_rp_table                                                                 #
#       Adds data to the RPS table based on provided rp_records. In cases where     #
#       the rp_name is already in the table, it updates the data for that row.      #
#   Args:                                                                           #
#       rp_recods {list{dict}}: A list of dict items where each key in the dict     #
#           is a column in the RPS table (returned from create_rp_table_records())  #
#####################################################################################
@edit_db.connection_context()
def update_rp_table(rp_records):
    with edit_db.atomic():
        RPS.insert_many(rp_records).on_conflict(
            conflict_target=[RPS.rp_name],
            preserve=[RPS.rp_name]
        ).execute()


if __name__ =="__main__":
    pass