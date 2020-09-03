import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

# import the data
data = pd.read_csv('data/Lagan_data.csv', infer_datetime_format='CREATED_DT')
# ensure that the data/time format is in a useful format
data['CREATED_DT'] = pd.to_datetime(data['CREATED_DT'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
# make the date dd/mm/yyyy format
data['CREATED_DT'] = data['CREATED_DT'].dt.date
# split the classification title into a subject, reason and type using the '-'/'|' as the delimnator
data[['Subject', 'Reason', 'Type']] = data['TITLE'].str.split(pat='-', expand=True)


subject_counts = data['Subject'].value_counts()
subject_mean = data['Subject'].value_counts().mean()

# Create a pivot table for overall cases raised by date
overall_cases = pd.pivot_table(data, index='CREATED_DT', values='CASE_REFERENCE', aggfunc='count')

# Create some datetime veriable for filters

# 01-01-2019 to 31-08-2019
year_a_start = pd.to_datetime('2019-01-01').date()
year_a_end = pd.to_datetime('2019-08-31').date()

# 01-01-2020 to 31-08-2020
year_b_start = pd.to_datetime('2020-01-01').date()
year_b_end = pd.to_datetime('2020-08-31').date()

# 01-01-2019 to 31-12-2020
year_19_start = pd.to_datetime('2019-01-01').date()
year_19_end = pd.to_datetime('2019-12-31').date()

# COVID Period
covid_start = pd.to_datetime('2020-03-01').date()
covid_end = pd.to_datetime('2020-08-31').date()

# Previous Period 2020
pp_start = pd.to_datetime('2019-03-01').date()
pp_end = pd.to_datetime('2019-08-31').date()

# Split the overall cases
year_a = overall_cases.loc[year_a_start:year_a_end]
year_b = overall_cases.loc[year_b_start:year_b_end]
year_19 = overall_cases.loc[year_19_start:year_19_end]

covid_period = overall_cases.loc[covid_start:covid_end]
previous_period = overall_cases.loc[pp_start:pp_end]

overall_cases.to_csv('data/overall_cases.csv')

# CLASSIFICATIONS
# Create Pivot Table
class_counts = pd.pivot_table(data, index='CREATED_DT', columns='Subject', values='CASE_REFERENCE', aggfunc='count', fill_value=0)
#  Drop any columns where the total number of cases raised is less than 100
class_counts.drop([col for col, val in class_counts.sum().iteritems() if val < 100], axis=1, inplace=True)

# Slice to specific reportable periods
class_covid = class_counts.loc[covid_start:covid_end]
class_pp = class_counts.loc[pp_start:pp_end]

class_covid.drop([col for col, val in class_covid.sum().iteritems() if val < 100], axis=1, inplace=True)
class_covid.to_csv('data/class_covid.csv')


# function to calculate rolling averages based on cases per day df


def rolling_calculations(input_df):
    """Calculates rolling averages over 3/5/7 days and outputs csv file"""
    input_df['3-day Avg'] = input_df['CASE_REFERENCE'].rolling(window=3).mean().round(2)
    input_df['5-day Avg'] = input_df['CASE_REFERENCE'].rolling(window=5).mean().round(2)
    input_df['7-day Avg'] = input_df['CASE_REFERENCE'].rolling(window=7).mean().round(2)
    input_df['10-day Avg'] = input_df['CASE_REFERENCE'].rolling(window=10).mean().round(2)


rolling_calculations(year_a)
rolling_calculations(year_b)
rolling_calculations(year_19)
