from ..models import edit_db
from ..models.software import Software
from ..models.aiSoftwareInfo import AISoftwareInfo
import pandas as pd 
from pandas._libs.parsers import STR_NA_VALUES
import os
import re


#################################################################################
#   lowercase_file_names                                                        #
#       Converts all file names in a given directory to lowercase.              #
#   Args:                                                                       #
#       dir_path {string}: path to the directory where the files are located    #
#################################################################################
def lowercase_file_names(dir_path):
    for file in os.listdir(dir_path):
        os.rename(dir_path + file, dir_path + file.lower())


#################################################################################
#   add_ai_example_use_to_df                                                    #
#       Matches software name with example use file from the EXAMPLE_USE_DIR    #
#       and adds the example use info to a pandas.DataFrame.                    #
#       Called directly from create_ai_software_table_records.                  #
#   Args:                                                                       #
#       df {pandas.DataFrame}: dataframe with an empty ai_example_use column    #
#           and some software column that has software names                    #
#   Function:                                                                   #
#       lowercase_file_names: Converts all filenames in a given location to     #
#           lowercase.                                                          #
#   Return:                                                                     #
#       df {pandas.DataFrame}: Input dataframe with filled ai_example_use col   #
#################################################################################
EXAMPLE_USE_DIR = "./data/exampleUse/"
def add_ai_example_use_to_df(df, software_column_name):
    
    software_names = df[software_column_name].tolist()

    # All softwares are lowercased so files should be lowercased to match
    lowercase_file_names(EXAMPLE_USE_DIR)

    for software in software_names:
        software_file_path = f"{EXAMPLE_USE_DIR}/{software}.txt"
        try:
            with open(software_file_path,'r') as s:
                data = s.read()
                df.loc[df[software_column_name] == software, "ai_example_use"] = data

        except FileNotFoundError:
            print(f"No example use file found for {software} in {EXAMPLE_USE_DIR}")
            continue

    return df

#################################################################################
#   create_ai_software_table_records                                            #
#       Creates 'records' of ai software info to add to the database. Each      #
#       record uses the information from the SOFTWARE_TABLE_CSV file.           #
#       The AI example use is added using the information from the data folder. #
#       The columns are renamed to match the AISoftwareInfo table.              #
#   Args:                                                                       #
#       columns {list}: A list of columns in the SOFTWARE_TABLE_CSV file that   #
#           we want to keep.                                                    #
#   Function:                                                                   #
#       add_ai_example_use_to_df: Takes in as input a pandas.Dataframe with all #
#           columns present and renamed (except Software col). adds example use #
#           info to the dataframe and returns it.                               #
#   Return:                                                                     #
#       records {list{dict}}: list of records to be added to the Software       #
#           table. The keys of the dict are columns in the table.               #
#################################################################################
SOFTWARE_TABLE_CSV = "./data/CSV/softwareTable.csv"
# TODO: This is a temporary function that gets data from the csv file. Should be changed to get data directly from the stuff in the `data` directory
def create_ai_software_table_records(columns=None):

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
    
    if columns:
        current_df_columns = set(df.columns.tolist())
        columns_to_remove = list(current_df_columns - columns)  # list of columns not in `columns`

        df = df.drop(columns=columns_to_remove)
    
    # rename the columns to match the db software table columns
    df = df.rename(columns={"✨Software Type":"ai_software_type", 
                       "✨Software Class":"ai_software_class",
                       "✨Research Field":"ai_research_field",
                       "✨Research Area":"ai_research_area",
                       "✨Research Discipline":"ai_research_discipline",
                       "✨Core Features": "ai_core_features",
                       "✨General Tags": "ai_general_tags",
                       "✨AI Description": "ai_description",
                       "✨Example Use": "ai_example_use",
                       })
    
    df = add_ai_example_use_to_df(df, 'Software')

    # Replace software names with software id
    software_names = df['Software'].tolist()

    for s in software_names:
        software_id = Software.get(Software.software_name == s)
        df.Software = df.Software.replace(s,software_id)
    df = df.rename(columns={"Software": "software_id"})

    df = df.fillna("")

    ai_software_records = df.to_dict('records')
    return ai_software_records


@edit_db.connection_context()
def update_ai_software_table(ai_software_records):

    with edit_db.atomic():
        AISoftwareInfo.insert_many(ai_software_records).on_conflict(
            conflict_target=[AISoftwareInfo.software_id],  # If there is a conflict on the `Unique` constraint of software_id
            preserve=[AISoftwareInfo.ai_description, 
                        AISoftwareInfo.ai_software_type, 
                        AISoftwareInfo.ai_software_class, 
                        AISoftwareInfo.ai_research_field,
                        AISoftwareInfo.ai_research_area,
                        AISoftwareInfo.ai_research_discipline,
                        AISoftwareInfo.ai_core_features,
                        AISoftwareInfo.ai_general_tags,
                        AISoftwareInfo.ai_example_use]   # Update the existing ai_software entry using the incomming (new) data
        ).execute()


if __name__=="__main__":
    pass