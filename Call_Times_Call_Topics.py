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
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#%%

"""
Importing the data files, stored locally on machine but available through GitHub
"""

file = "311_Contact_Management_Cases.csv"
file2 = "311_Call_Center_Activity_by_Day.csv"
file3 = "311 Calls 092916_061518_scrub.csv"
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



#%%
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
"""
Transform date-times to date-time class in case dataset
"""

print(case_data.info())
print(case_data.iloc[:, 1].head())
time_format = '%Y-%m-%d %H:%M'
case_data.Entry_Date___Calc = pd.to_datetime(case_data.Entry_Date___Calc,format = time_format)
case_data.Close_Date___Calc = pd.to_datetime(case_data.Close_Date___Calc, format = time_format)

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

sns.set_style("white")
_ = sns.swarmplot(x='Day_of_Week', y='Total_Calls_Handled', data=daily_data)
_.set(xlabel="Day of the Week", ylabel="Number of Calls", xticklabels=['Mon','Tue','Wed','Thu','Fri'])
plt.show()



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


monthly_call_mean = daily_data.groupby('Month_of_Year', as_index=False)['CallsPresented'].mean().reset_index(drop=True)
monthly_call_mean = monthly_call_mean.sort_values('CallsPresented', ascending=False).reset_index(drop=True)

plt.bar(monthly_call_mean['Month_of_Year'], monthly_call_mean['CallsPresented'], color = sns.color_palette())
plt.title("Average Daily Call Volume by Month over 2013-2015")
plt.xlabel("Month")
plt.ylabel('Average Number of Calls Presented')
plt.show()
plt.savefig('Monthly_Call_Avg.png')


#%%
"""
T-test comparing two extreme samples: July and March
"""
from scipy import stats

jul = daily_data.loc[daily_data['Month_of_Year'] == 'Jul']
jul_calls = jul.CallsPresented.values

mar = daily_data.loc[daily_data['Month_of_Year'] == 'Mar']
mar_calls = mar.CallsPresented.values

print("The null hypothesis states that no statistically significant difference\
 exists between the number of calls in July and March")

print(np.var(mar_calls))
print(np.var(jul_calls))
# These variances are very close, the test is run assuming same and different variances
# The same result is yielded in both cases

jul_mar_ttest = stats.ttest_ind(jul_calls, mar_calls)

print("The two-sample t-test yields a t statistic of " + str(round(jul_mar_ttest[0], 2)) + ".")
print("The corresponding p-value is nearly zero.  This disproves the null hypothesis.\
  In this case, the difference in average call volume between July and March\
 is significant.")

apr = daily_data.loc[daily_data['Month_of_Year'] == 'Apr']
apr_calls = apr.CallsPresented.values

print(np.var(apr_calls))
print(np.var(jul_calls))

apr_jul_ttest = stats.ttest_ind(apr_calls, jul_calls, equal_var=False)

print("The same difference does not hold true for April and July, two high volumes months.")


#%%
"""
Call resolution by topic
"""
# Preprocessing to a concise dataframe

print(article_data.columns)
topics = article_data.drop(columns=['(Do Not Modify) Phone Call', '(Do Not Modify) Row Checksum', '(Do Not Modify) Modified On', 'Created On'])
topics.columns = ['Topic', 'Duration', 'KB_Article']
topics.columns

#%%
"""
Initializing function to change string duration of X:XX to seconds numeric
"""


def string_to_sec(df, col_name):
    ''' 
    This function accepts a dataframe and column name (in quotes)
    It converts the column from XX:XX:XX to seconds and returns in list
    Pandas must be imported and aliased as pd
    '''
    new = []
    for i in range(len(df[col_name])):
        x = df.loc[i][col_name]
        if x.count(":") == 1:
            ''' For Min:sec '''
            y, z = x.split(":")
            y = pd.to_numeric(y)
            z = pd.to_numeric(z)
            q = (y * 60) + z
        elif x.count(":") == 2:
            ''' For H/Min:Min/sec:Sec/Nothing '''
            h, y, z = x.split(":")
            if len(h) == 2:
                ''' This assumes if the first number is 2 digits, it is min'''
                h = pd.to_numeric(h)
                y = pd.to_numeric(y)
                q = (h * 60) + y
            elif len(h) == 1:
                '''Assuming first digit is single, means hours'''
                h = pd.to_numeric(h)
                y = pd.to_numeric(y)
                z = pd.to_numeric(z)
                q = (h * 3600) + (y * 60) + z
            else:
                q = np.NaN
        else:
            q = np.NaN
        new.append(q)
    return new

#%%
"""
Add a column called 'Seconds' that represents duration as seconds in numeric form
"""

topics['Seconds'] = string_to_sec(topics, 'Duration')
sum(topics['Seconds'] == np.NaN)
print(topics.Seconds.mean())

#%%
"""
Grouping calls by KB owner to take quick mean of duration
"""

topics_grouped_kb_owner = topics.groupby('KB_Article', as_index=False)['Seconds'].mean()
print(topics_grouped_kb_owner)
topics_grouped_kb_owner = topics_grouped_kb_owner.sort_values(by=['Seconds'], ascending=False).reset_index(drop=True)
plt.bar(topics_grouped_kb_owner['KB_Article'][0:5], topics_grouped_kb_owner['Seconds'][0:5], color=sns.color_palette('deep'))
plt.title("Top Departments by Call Duration")
plt.xticks([0,1,2,3,4], ['Kheran Joseph', 'Code Enforcement', 'Parks', 'Mayor\'s Office', 'Engineering'], rotation=45)
plt.xlabel("KB Team")
plt.ylabel("Average Call Duration")
plt.show()
#plt.savefig('Call_Dur_by_Dept.png')


#%%
"""
Identifying Number of calls by department
"""
topics_count = topics.groupby('KB_Article', as_index=False)['Topic'].count()
topics_count = topics_count.sort_values(by=['Topic'], ascending=False).reset_index(drop=True)
plt.bar(topics_count['KB_Article'][0:5], topics_count['Topic'][0:5], color = sns.color_palette())
#loc, lab = plt.xticks()
plt.xticks([0,1,2,3,4],['Solid Waste', 'Water Works', 'Streets', 'Adoxio', 'Lucy McFarlane'], rotation = 45),
plt.title("Total Call Volume by Department \n 5 Highest")
plt.xlabel("Department")
plt.ylabel("Total Call Volume")
#plt.savefig('Call_Vol_by_Dept.png')
plt.show()

#%%
"""
Exploring the number of calls by topic
"""
tt = topics
tt['Count'] = 1
tt_count = topics.groupby('Topic', as_index=True)['Count'].count()
tt_count = tt_count.sort_values(ascending=False)
print(tt_count.head())
tt_count = tt_count.to_frame()
tt_count['Percentage'] = tt_count.Count.apply(lambda x: round(x/np.sum(tt_count['Count'])*100,2))

#%%
"""
Finishing dataframe to show average duration and total number of calls by topic
"""
temp = topics.groupby('Topic', as_index=True)['Seconds'].mean()
goal = pd.concat([tt_count, temp], axis=1, join='inner')
goal.head()

"""
Pairing each topic with KB team owner for visualization purposes
"""
temp = topics.groupby(['Topic', 'KB_Article'], as_index=True)['Seconds'].count()
temp = temp.to_frame()
temp = temp.reset_index()
temp.index = temp['Topic']
temp = temp.drop(columns=['Topic', 'Seconds'])
print(temp.info())

# Join to the main goal frame for plotting purposes

final = pd.merge(goal, temp, how='left', left_index=True, right_index=True)
final.info()
#final.to_csv('final_groups.csv')

"""
Had to pull into Excel to remove duplicate rows.
Need to investigate why pandas is doing this
"""

topic_data = pd.read_csv('final_groups.csv')


