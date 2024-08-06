from ..models import db
from ..models.software import Software
import pandas as pd
from pandas._libs.parsers import STR_NA_VALUES
SOFTWARE_TABLE_CSV = "./data/CSV/softwareTable.csv"

# TODO: This is a temporary function that gets data from the csv file. Should be changed to get data directly from the stuff in the `data` directory
def get_software_table_records(columns=None):

    try:
        # Ookami has a software called null...wtf
        # the code below tells pandas to not treat 'null' as NaN or NULL value

        # Get the default list of NA values
        default_na_values = list(STR_NA_VALUES)
        custom_na_values = [v for v in default_na_values if v != 'null']
        df = pd.read_csv(SOFTWARE_TABLE_CSV, keep_default_na=False, na_values=custom_na_values)

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

    print(df[df['software_name'].isnull()])

    
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
coutner = 0
for s in software:
    # print(f"software: {s.software_name}, \
    #       desc: {s.software_description}, \
    #       web_p: {s.software_web_page}, \
    #       s_doc: {s.software_documentation},\
    #       s_use_link: {s.software_use_link}"
    #       )
    coutner += 1

print(coutner)

if __name__ =="__main__":
    pass