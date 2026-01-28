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
    """Modify a clomn 'Sum of Volume' to 'VOLUME' and convert it to type Int64 """
    df.rename(columns = {'Sum of Volume' : VOLUME}, inplace = True)
    df[VOLUME] = df[VOLUME].astype('Int64')

def clean_region(df: pd.DataFrame) -> None:
    """Modify 'QuÈbec' and 'Quebec' to 'Québec' and remove the word 'Region' """
    df[REGION] = df[REGION].replace({'QuÈbec Region': 'Québec Region','Quebec Region': 'Québec Region'})
    df[REGION] = df[REGION].str.replace(' Region','')

def clean_port(df: pd.DataFrame) -> None:
    """ Split 'Port of Entry' columns into 'PORT_ID and 'PORT_NAME and delete original 'Port of Entry' column"""
    spl = df['Port of Entry'].str.split('-', expand = True)
    df[PORT_ID] = spl[0].str.strip().astype(int)
    df[PORT_NAME] = spl[1].str.strip()
    df.drop(columns = ['Port of Entry'], inplace = True)

def clean_data (df: pd.DataFrame) -> None:
    """ Convert Date column to datetime and calling clean_region, clean_volume, and clean_port to complete data cleaning tasks"""
    df[DATE] = pd.to_datetime(df[DATE])
    clean_region(df)
    clean_volume(df)
    clean_port(df)

def fill_missing_volumes(df: pd.DataFrame, strategy: str) -> None:
    """ Modify df by filling missing values in the VOLUME column using the specified strategy. """
    if strategy == MEAN:
        df[VOLUME] = df[VOLUME].fillna(round(df[VOLUME].mean()))
    elif strategy == MEDIAN:
        df[VOLUME] = df[VOLUME].fillna(round(df[VOLUME].median()))
    else:
        df[VOLUME] = df[VOLUME].fillna(0)
    

### Task 2: Data Exploration and Analysis Functions ###

def filter_with_volume(df: pd.DataFrame, col: str, val: str, vol: int) -> pd.DataFrame:
    """"""
    fil = (df[col] == val) & (df[VOLUME] >= vol)
    return df[fil]

def find_port_name(df: pd.DataFrame, id: int) -> str:
    """"""
    row = df[df[PORT_ID] == id]
    return row[PORT_NAME][0]

def get_mean_volume_by(df: pd.DataFrame, col: str) -> pd.Series:
    """"""
    return df.groupby[col][VOLUME].mean()

def get_top_n_by_volume(df: pd.DataFrame, col: str, n: int) -> pd.Series:
    total = df.groupby(col)[VOLUME].sum()
    order = total.sort_values(ascending = False)
    return order.head(n)

def compute_volume_by_time(df: pd.DataFrame, col: str, year: int, month: int) -> pd.Series:
    """"""
    f_year = df[DATE].dt.year == year
    if month != -1:
        f_year = f_year & (df[DATE].dt.month == month)
    f_df = df[f_df]
    return f_df.groupby(col)[VOLUME].sum()

def calculate_volume_change(df: pd.DataFrame, col: str, in_year: int, in_month: int, fi_year: int, fi_month: int) -> pd.Series:
    return compute_volume_by_time(df, col, fi_year, fi_month) - compute_volume_by_time(df, col, in_year, in_month)


if __name__ == "__main__":
    pass 

    # You may call on your functions here to test them.

    border_df = load_data('traveller-report-daily.csv')
    clean_data (border_df)
    fill_missing_volumes(border_df, MEAN)