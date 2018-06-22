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
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.plotting import figure
# need to import the rest of bokeh here

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
"""

print(case_data.columns)
print(case_data.info())
print(case_data.describe())
#%%
print(daily_data.columns)
print(daily_data.info())
print(daily_data.describe())
#%%
print(article_data.columns)
print(article_data.info())
print(article_data.describe())

#%%
"""
