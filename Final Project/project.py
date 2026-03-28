import pandas as pd
import numpy as np
import sqlite3

def load_and_preprocess_data(hr_path, market_path):
    """Loads and cleans both HR and Market datasets."""
    hr = pd.read_csv(hr_path)
    market = pd.read_csv(market_path)
    
    edu_to_numeric = {
        "High School": 1,
        "Associate's Degree": 2, "Associate's": 2,
        "Bachelor's": 3, "Bachelor's Degree": 3,
        "Master's": 4, "Master's Degree": 4,
        "PhD": 5, "phD": 5
    }
    market['Education'] = market['Education Level'].map(edu_to_numeric)
    market = market.dropna(subset=['Education'])
    market['Education'] = market['Education'].astype(int)
    hr = hr.dropna(subset=['MonthlyIncome', 'Department', 'JobRole'])
    
    return hr, market

def setup_database(hr_df, market_df, db_name='attrition_analysis.db'):
    """Creates a local SQLite database for the analysis."""
    conn = sqlite3.connect(db_name)
    hr_df.to_sql('internal_hr', conn, if_exists='replace', index=False)
    market_df.to_sql('market_salary', conn, if_exists='replace', index=False)
    return conn

def run_causal_analysis(conn):
    """Executes the main query comparing internal vs market pay and attrition."""
    query = """
    SELECT 
        h.Education as Edu_Level,
        h.OverTime,
        AVG(h.MonthlyIncome) as Internal_Pay,
        AVG(m.Salary / 12) as Market_Pay_Avg,
        (AVG(h.MonthlyIncome) - AVG(m.Salary / 12)) as Monthly_Pay_Gap,
        AVG(CASE WHEN h.Attrition = 'Yes' THEN 1.0 ELSE 0.0 END) * 100 as Attrition_Percent
    FROM internal_hr h
    JOIN market_salary m ON h.Education = m.Education
    GROUP BY h.Education, h.OverTime
    """
    return pd.read_sql_query(query, conn)

def get_role_pay_gap(conn, edu_level=4):
    """Analyzes pay gaps by Job Role for a specific education level (default: Master's)."""
    query = """
    SELECT 
        h.JobRole,
        AVG(h.MonthlyIncome) as Internal_Avg,
        AVG(m.Salary / 12) as Market_Avg,
        (AVG(h.MonthlyIncome) - AVG(m.Salary / 12)) as Pay_Difference
    FROM internal_hr h
    JOIN market_salary m ON h.Education = m.Education
    WHERE h.Education = ?
    GROUP BY h.JobRole
    ORDER BY Pay_Difference ASC
    """
    return pd.read_sql_query(query, conn, params=(edu_level,))

def get_department_burnout(conn):
    """Analyzes attrition rates by department and overtime status."""
    query = """
    SELECT 
        Department,
        OverTime,
        COUNT(*) as Total_Staff,
        AVG(CASE WHEN Attrition = 'Yes' THEN 1.0 ELSE 0.0 END) * 100 as Attrition_Rate
    FROM internal_hr
    GROUP BY Department, OverTime
    """
    return pd.read_sql_query(query, conn)