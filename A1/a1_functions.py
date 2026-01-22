"""CSC108: Winter 2026 -- Assignment 1: Canadian Border Crossings

This code is provided solely for the personal and private use of students
taking the CSC271H1 course at the University of Toronto. Copying for purposes
other than this use is expressly prohibited. All forms of distribution of
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2026 CSC271H1 Teaching Team
"""

import pandas as pd
import numpy as np

# Column labels
DATE = 'Date'
REGION = 'Region'
MODE = 'Mode'
VOLUME = 'Volume'
PORT_ID = 'Port ID'
PORT_NAME = 'Port Name'

# Fill strategies
MEAN = 'mean'
MEDIAN = 'median'
ZERO = 'zero'

### Provided Helper Function ###

def load_data(file_path: str) -> pd.DataFrame:
    """Return the data from the CSV file named file_path as a DataFrame."""

    return pd.read_csv(file_path)

### Task 1: Data Cleaning and Preparation ###


### Task 2: Data Exploration and Analysis Functions ###


if __name__ == "__main__":
    pass 

    # You may call on your functions here to test them.

    border_df = load_data('traveller-report-daily.csv')
    #clean_data(border_df)
    #fill_missing_volumes(border_df)