import json
import glob
import os
import pandas as pd
import numpy as np
from models.software import Software

CURATED_INPUT_DIRECTORY = './data/CSV/ACCESS_Software.csv'


def parse_curated_csv(return_columns=None):

    df = pd.read_csv(CURATED_INPUT_DIRECTORY, na_filter=False)

    # Ensure uniform capitalization across cells
    df['RP Name'] = df['RP Name'].str.title()
    df['Software Type'] = df['Software Type'].str.title()
    df['Software Class'] = df['Software Class'].str.title()
    df['Research Area'] = df['Research Area'].str.title()
    df['Research Discipline'] = df['Research Discipline'].str.title()

    # Table Column Formatting
    df.rename(columns={'Software Documentation/Link' : 'Software Documentation'}, inplace=True)
    df.rename(columns={'Example Software Use (link)' : 'Example Software Use'}, inplace=True)

        # Description Source Formatting
    df['Software Description'] = df['Software Description'].str.replace(
        'Description Source:', '\nDescription Source: ')

    # Make Example Links on separate lines
    df['Example Software Use'] = df['Example Software Use'].str.replace(' , ', ' \n')

    # Columns:['Software', 'RP Name', 'Software Type', 'Software Class',
    #   'Research Area', 'Research Discipline', 'Software Description',
    #   'Software's Web Page', 'Software Documentation',
    #   'Example Software Use']

    