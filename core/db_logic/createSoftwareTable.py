from models import db
from models.software import Software
import pandas as pd

SOFTWARE_TABLE_CSV = "./data/CSV/softwareTable.csv"

# TODO: This is a temporary function that gets data from the csv file. Should be changed to get data directly from the stuff in the `data` directory
def get_software_table_records(columns=None):

    try:
        df = pd.read_csv(SOFTWARE_TABLE_CSV)
    except:
        print("Software table not found")
        return None
    
    if columns:

        current_df_columns = set(df.columns.tolist())
        columns_to_remove = list(current_df_columns - columns)

        df = df.drop(columns=columns_to_remove)
    
    # rename the columns to match the db software table columns
    df = df.rename(columns={"Software":"software_name", 
                       "Software Description":"software_description",
                       "Software's Web Page":"software_web_page",
                       "Software Documentation":"software_documentation",
                       "Example Software Use":"software_use_link"})

    df = df.fillna("")

    software_records = df.to_dict('records')

    return software_records

@db.connection_context()
def create_software_table():
    db.drop_tables([Software])
    db.create_tables([Software])

@db.connection_context()
def update_software_table(software_records):

    Software.insert_many(software_records).on_conflict(
        conflict_target=[Software.software_name],  # If there is a conflict on the `Unique` constraint of rp_name
        preserve=[Software.software_description, 
                  Software.software_web_page, 
                  Software.software_documentation, 
                  Software.software_use_link]   # Update the existing rp entry using the incomming (new) data
    ).execute()


columns={'Software',"Software Description","Software's Web Page","Software Documentation","Example Software Use"}
software_records = get_software_table_records(columns)
create_software_table()
update_software_table(software_records)

software = Software.select()

for s in software:
    print(f"software: {s.software_name}, \
          desc: {s.software_description}, \
          web_p: {s.software_web_page}, \
          s_doc: {s.software_documentation},\
          s_use_link: {s.software_use_link}"
          )


if __name__ =="__main__":
    pass