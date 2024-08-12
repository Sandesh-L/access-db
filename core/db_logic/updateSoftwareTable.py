from ..models import edit_db
from ..models.software import Software
import pandas as pd
from pandas._libs.parsers import STR_NA_VALUES


#################################################################################
#   create_software_table_records                                               #
#       Creates 'records' of software to add to the database. Each record uses  #
#       the descripitons, links, and softwares from the SOFTWARE_TABLE_CSV file.#
#       Software is also added from the parsed_spider_output and any duplicates #
#       are removed.                                                            #
#   Args:                                                                       #
#       columns {list}: A list of columns in the SOFTWARE_TABLE_CSV file that   #
#           we want to keep.                                                    #
#       parsed_spider_output {Dict}: A dictionary with rp name as the key       #
#           and a tuple of software and versions as the values (returned from   #
#           parse_spider_output function)                                       #
#                                                                               #
#    Return:                                                                    #
#        records {list{dict}}: list of records to be added to the Software      #
#                table. The keys of the dict are columns in the table.          #
#################################################################################
# TODO: This is a temporary function that gets data from the csv file. Should be changed to get data directly from the stuff in the `data` directory
SOFTWARE_TABLE_CSV = "./data/CSV/softwareTable.csv"
def create_software_table_records(columns, parsed_spider_output):

    try:
        # Ookami has a software called 'null'...
        # the code below tells pandas to not treat 'null' as NaN or NULL value

        # Get the default list of NA values
        default_na_values = list(STR_NA_VALUES)
        custom_na_values = [v for v in default_na_values if v != 'null']
        df = pd.read_csv(SOFTWARE_TABLE_CSV, keep_default_na=False, na_values=custom_na_values)

    except:
        print("Software table not found")
        return None
    
    # we only want specific columns from the csv file
    current_df_columns = set(df.columns.tolist())
    columns_to_remove = list(current_df_columns - columns)
    df = df.drop(columns=columns_to_remove)

    # rename the columns to match the db software table columns
    df = df.rename(columns={"Software":"software_name", 
                       "Software Description":"software_description",
                       "Software's Web Page":"software_web_page",
                       "Software Documentation":"software_documentation",
                       "Example Software Use":"software_use_link"})
    
    # Add softwares from spider output
    # parsed_spider_output is in the format {rp_name: (softwareName, softwareVersion)}
    software = []
    for rp in parsed_spider_output.keys():
        for item in parsed_spider_output[rp]:
            software.append(item[0])    # get only the software name

    spider_df = pd.DataFrame(software, columns=['software_name'])
    
    # Combine unique values from both DataFrames' 'software_name'
    combined_softwares = pd.concat([df['software_name'], spider_df['software_name']]).drop_duplicates().reset_index(drop=True)
    software_name_df = pd.DataFrame({'software_name': combined_softwares})
    software_df = software_name_df.merge(df, on="software_name", how='left')

    software_df = software_df.fillna("")

    software_records = software_df.to_dict('records')
    return software_records


#################################################################################
#   update_software_table                                                       #
#       Adds data to the Software table based on provided software_records.     #
#       In cases where the software_name is already in the table, it updates    #
#       the data for that row.                                                  #
#   Args:                                                                       #
#       software_records {list{dict}}: A list of dict items where each key in   #
#           the dict is a column in the RPS table (returned from                #
#           create_software_table_records())                                    #
#################################################################################
@edit_db.connection_context()
def update_software_table(software_records):
    
    with edit_db.atomic():
        Software.insert_many(software_records).on_conflict(
            conflict_target=[Software.software_name],  # If there is a conflict on the `Unique` constraint of rp_name
            preserve=[Software.software_description, 
                    Software.software_web_page, 
                    Software.software_documentation, 
                    Software.software_use_link]   # Update the existing rp entry using the incomming (new) data
        ).execute()

if __name__ =="__main__":
    pass