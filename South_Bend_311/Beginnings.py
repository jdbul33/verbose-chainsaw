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

import pandas as pd

file = "C://users/jdbul/Documents/GitHub/Verbose-Chainsaw/311_Contact_Management_Cases.csv"
file2 = "C://users/jdbul/Documents/GitHub/Verbose-Chainsaw/311_Call_Center_Activity_by_Day.csv"
case_data = pd.read_csv(file)
daily_data = pd.read_csv(file2)