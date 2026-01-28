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

def clean_volume(df: pd.DataFrame) -> None:
    """
    Modify a clomn 'Sum of Volume' to 'VOLUME' and convert it to type Int64 
    Parameter: df 
    """
    df.rename(columns = {'Sum of Volume' : VOLUME}, inplace = True)
    df[VOLUME] = df[VOLUME].astype('Int64')

def clean_region(df: pd.DataFrame) -> None:
    """
    Modify 'QuÈbec' and 'Quebec' to 'Québec' and remove the word 'Region' 
    Parameter: df
    """
    df[REGION] = df[REGION].replace({'QuÈbec Region': 'Québec Region','Quebec Region': 'Québec Region'})
    df[REGION] = df[REGION].str.replace(' Region','')

def clean_port(df: pd.DataFrame) -> None:
    """ 
    Split 'Port of Entry' columns into 'PORT_ID and 'PORT_NAME and delete original 'Port of Entry' column
    Parameter: df
    """
    spl = df['Port of Entry'].str.split('-', expand = True)
    df[PORT_ID] = spl[0].str.strip().astype(int)
    df[PORT_NAME] = spl[1].str.strip()
    df.drop(columns = ['Port of Entry'], inplace = True)

def clean_data (df: pd.DataFrame) -> None:
    """ 
    Convert Date column to datetime and calling clean_region, clean_volume, and clean_port to complete data cleaning tasks
    Parameter: df
    """
    df[DATE] = pd.to_datetime(df[DATE])
    clean_region(df)
    clean_volume(df)
    clean_port(df)

def fill_missing_volumes(df: pd.DataFrame, strategy: str) -> None:
    """ 
    Modify df by filling missing values in the VOLUME column using the specified strategy
    Parameter: df, strategy
    """
    if strategy == MEAN:
        df[VOLUME] = df[VOLUME].fillna(round(df[VOLUME].mean()))
    elif strategy == MEDIAN:
        df[VOLUME] = df[VOLUME].fillna(round(df[VOLUME].median()))
    else:
        df[VOLUME] = df[VOLUME].fillna(0)
    

### Task 2: Data Exploration and Analysis Functions ###

def filter_with_volume(df: pd.DataFrame, col: str, val: str, vol: int) -> pd.DataFrame:
    """
    Return the rows of df where the value in col is equal to val and the volume is greater than or equal to vol
    Parameters: df, col, val, vol
    """
    fil = (df[col] == val) & (df[VOLUME] >= vol)
    return df[fil]

def find_port_name(df: pd.DataFrame, id: int) -> str:
    """
    Return the port name in df that corresponds to the given port_id
    Parameter: df, id
    """
    row = df[df[PORT_ID] == id]
    return row[PORT_NAME][0]

def get_mean_volume_by(df: pd.DataFrame, col: str) -> pd.Series:
    """
    Return a series of the mean volumes for each group in col from df
    Parameter: df, col
    """
    return df.groupby(col)[VOLUME].mean()

def get_top_n_by_volume(df: pd.DataFrame, col: str, n: int) -> pd.Series:
    """
    Return a series of total volumes from df for the top n groups in col
    Parameter: df, col, n
    """
    total = df.groupby(col)[VOLUME].sum()
    order = total.sort_values(ascending = False)
    return order.head(n)

def compute_volume_by_time(df: pd.DataFrame, col: str, year: int, month: int) -> pd.Series:
    """
    Return a series of total volume from df per group in col for the year and month
    Parameter: df, col, year, month
    """
    f_year = df[DATE].dt.year == year
    if month != -1:
        f_year = f_year & (df[DATE].dt.month == month)
    f_df = df[f_year]
    return f_df.groupby(col)[VOLUME].sum()

def calculate_volume_change(df: pd.DataFrame, col: str, in_year: int, in_month: int, fi_year: int, fi_month: int) -> pd.Series:
    """
    Return a series of volume changes in df for groups in col between the initial and final periods
    Parameter: df, col, in_year, in_month, fi_year, fi_month
    """
    return compute_volume_by_time(df, col, fi_year, fi_month) - compute_volume_by_time(df, col, in_year, in_month)


if __name__ == "__main__":
    pass 

    # You may call on your functions here to test them.

    border_df = load_data('traveller-report-daily.csv')
    clean_data (border_df)
    fill_missing_volumes(border_df, MEAN)