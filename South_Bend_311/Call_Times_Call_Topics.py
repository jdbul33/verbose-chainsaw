# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 12:12:03 2018

@author: jdbul
"""

"""
This file is to run after initialization in beginnings.py
Analyzing resolution times of calls
by topic and department
"""
#%%
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


#%%
"""
Transform date-times to date-time class in case dataset
"""

print(case_data.info())
print(case_data.iloc[:,1].head())
time_format = '%Y-%m-%d %H:%M'
case_data.Entry_Date___Calc = pd.to_datetime(case_data.Entry_Date___Calc,
                                             format = time_format)
case_data.Close_Date___Calc = pd.to_datetime(case_data.Close_Date___Calc,
                                             format = time_format)

#%%
"""
Transform index to date
"""

print(daily_data.info())
print(daily_data.iloc[:,0].head())
daily_data.Date = pd.to_datetime(daily_data.Date, format = '%Y-%m-%d')
print(daily_data.iloc[:,0].head())
daily_data.index = daily_data.Date
print(daily_data.info())
daily_data = daily_data.drop(columns = 'Date')
print(daily_data.head())

#%%
"""
Begin EDA for daily data to explore times, durations
"""

daily_data.plot(y='Avg_Handle_Time__seconds_')
plt.show()

plt.scatter(daily_data.Total_Calls_Handled, daily_data.Avg_Handle_Time__seconds_)
plt.show()

sns.swarmplot(x='Day_of_Week', y='Total_Calls_Handled', data=daily_data)
plt.show()

#Day 2 of week seems to have highest total number of calls.  Maybe Monday?
#mean_total_calls = []
#months = ['Jan', 'Feb', 'Mar', 'Apr', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

#for i in months:
#    x = np.mean(daily_data.Total_Calls_Handled[[daily_data.Month_of_Year[i]]])
#15    mean_total_calls.append(x)



daily_num = daily_data
daily_num = daily_num.drop(columns=['Day_of_Week', 'Month_of_Year', 'Year', 'Month_and_Year', 'FID'])
daily_num.info()

# The following plot code is only run once since it is saved locally

# _ = sns.pairplot(daily_num, kind='scatter')
# _.savefig('Daily_Data_PairPlot.png')

#%%
"""
Call volume by Month
"""


monthly_call_mean = daily_data.groupby('Month_of_Year', as_index=False)['CallsPresented'].mean()
print(monthly_call_mean)

plt.bar(monthly_call_mean['Month_of_Year'], monthly_call_mean['CallsPresented'], color = 'rgbmrgbmrgbm')
plt.title("Average Call Volume by Month over 2013-2015")
plt.xlabel("Month")
plt.ylabel('Average Number of Calls Presented')
#plt.show()
#plt.savefig('Monthly_Call_Avg.png')

"""
Call Volume by Year
"""


