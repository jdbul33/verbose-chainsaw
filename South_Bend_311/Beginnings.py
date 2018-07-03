# -*- coding: utf-8 -*-
"""
Created on Mon May 28 22:53:46 2018

@author: jdbul
"""

"""

An examination and exploration of the city of South Bend's 311 Customer Call 
Line, using publicly available data from 
https://data-southbend.opendata.arcgis.com

"""
#%%
import pandas as pd


"""
Importing the data files, stored locally on machine but available through GitHub
"""

file = "C://users/jdbul/Documents/GitHub/Verbose-Chainsaw/311_Contact_Management_Cases.csv"
file2 = "C://users/jdbul/Documents/GitHub/Verbose-Chainsaw/311_Call_Center_Activity_by_Day.csv"
file3 = "C://users/jdbul/Google Drive/Python Independent Study/311 Calls 092916_061518_scrub.csv"
case_data = pd.read_csv(file)
daily_data = pd.read_csv(file2)
article_data = pd.read_csv(file3)

#%%
"""
Evaluating basic data tidiness

Data will be imputed if necessary, but preferably dropped if minimal
"""

print(case_data.columns)
print(case_data.info())
print(case_data.describe())
case_data = case_data.dropna(axis = 0)
#Data dropped here since it only consisted of a small percentage of rows
print(case_data.info())
#%%
print(daily_data.columns)
print(daily_data.info())
print(daily_data.describe())
daily_data_mean = daily_data.mean()
daily_data = daily_data.fillna(daily_data_mean)
# Only 1 missing value in each of several columns here, easily imputed
print(daily_data.info())
#%%
print(article_data.columns)
print(article_data.info())
print(article_data.describe())
article_data = article_data.drop(columns = ['Regarding'])
#This column was categorical and missing over 180K entries

print(article_data.columns)
print(article_data.head())



