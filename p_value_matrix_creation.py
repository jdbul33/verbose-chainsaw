# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 22:19:19 2018

@author: jdbul
"""

import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

#%%

month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

calls = []
for i in range(len(month)):
    mon = daily_data.loc[daily_data['Month_of_Year'] == month[i]]
    calls.append(list(mon.CallsPresented.values))

monthly_calls = dict(zip(month, calls))

p_df = pd.DataFrame(index=month, columns=month)

for i in range(len(month)):
    for j in range(len(month)):
        res = stats.ttest_ind(monthly_calls[month[i]], monthly_calls[month[j]])
        p_df.iloc[i,j] = res[1]

p_df = p_df.apply(pd.to_numeric)

d = p_df.where(np.tril(np.ones(p_df.shape)).astype(np.bool))
fig = sns.heatmap(d, center = .05, cmap='coolwarm')
fig.set_title("P-Values from T-Test on Monthly Call Volume Distributions")
plot = fig.get_figure()
#plot.savefig('Heatmap.png')

#%%

df_list_m=[]
for i, data, name in zip([0,1,2,3,4, 5, 6, 7, 8, 9, 10 ,11],calls, month):
    d = {'Mean Daily Call Volume':data, 'Month':name}
    df = pd.DataFrame(data=d)
    df_list_m.append(df)

monthly_call_totals = pd.concat([i for i in df_list_m], ignore_index=True)   

#%%
sns.set(style="white")
sns.set_palette(sns.cubehelix_palette(12, start=2, rot=0, dark=.3, light=.85, reverse=True))

f=sns.boxplot(x='Month', y='Mean Daily Call Volume',
            data=monthly_call_totals)

sns.despine()

plot2=f.get_figure()
#plot2.savefig('Daily_Call_Boxplot')

#%%
"""
reuse code from bokeh to get call distributions
"""
df4 = topics
df4['Date'] = article_data['Created On']
df4['Date'] = pd.to_datetime(df4['Date'], format='%m/%d/%Y %H:%M')
df4['Date'] = df4['Date'].apply(lambda x: x.date())

day = []
for i in range(len(df4['Date'])):
    x = df4.iloc[i]['Date']
    x = x.weekday()+2
    day.append(x)
df4['Day_of_Week'] = day


temp1 = daily_data[['Day_of_Week', 'CallsPresented']].copy()
temp1 = temp1.reset_index(drop=True)
temp1.rename(columns={'CallsPresented': 'Count'}, inplace=True)
df4_1 = df4.groupby(['Date', 'Day_of_Week'], as_index=False)['Count'].count()
df4_1 = df4_1.drop(columns = ['Date'])

new_df = pd.concat([temp1, df4_1], ignore_index=True)

mon = np.array(new_df.Count[new_df['Day_of_Week'] == 2])
tue = np.array(new_df.Count[new_df['Day_of_Week'] == 3])
wed = np.array(new_df.Count[new_df['Day_of_Week'] == 4])
thu = np.array(new_df.Count[new_df['Day_of_Week'] == 5])
fri = np.array(new_df.Count[new_df['Day_of_Week'] == 6])

#%%


days=['Monday','Tuesday','Wednesday','Thursday','Friday']


df_list=[]
for i, data, name in zip([0,1,2,3,4],[mon, tue, wed, thu, fri], ['Monday','Tuesday','Wednesday','Thursday','Friday']):
    d = {'Mean Daily Call Volume':data, 'Day of the Week':name}
    df = pd.DataFrame(data=d)
    df_list.append(df)

daily_call_totals = pd.concat([i for i in df_list], ignore_index=True)   
    
#%%

sns.set(style="white")
sns.set_palette(sns.cubehelix_palette(5, start=2, rot=0, dark=.3, light=.85, reverse=True))

f=sns.boxplot(x='Day of the Week', y='Mean Daily Call Volume',
            data=daily_call_totals)

sns.despine()

plot2=f.get_figure()
#plot2.savefig('Daily_Call_Boxplot')

#%%

df = pd.DataFrame(topics.groupby('KB_Article', as_index=False)['Seconds'].sum())
#df['Percentage'] = round(df['Seconds']/sum(df['Seconds']) *100, 2)
df = df.sort_values('Seconds', ascending=False)
others = pd.Series([df.iloc[5:,1].sum()])
others = pd.Series(['All Other Departments', others[0]], index=['KB_Article', 'Seconds'])
df = df.append(others, ignore_index=True)
df = df.drop(df.index[5:23])
dept = list(df['KB_Article'])

for i in range(len(dept)):
    n = dept[i]
    dept[i] = n.replace(' - KB Team', '')
    
df['Department'] = dept
    
#df = df.set_index('KB_Article')

df['Total Call Time in Minutes'] = df['Seconds']//60
#%%
sns.set(style='whitegrid')
plt.figure(figsize=(6,4))
plt.tight_layout()
_ = sns.barplot(x='Department', y='Total Call Time in Minutes', data=df)
for item in _.get_xticklabels():
    item.set_rotation(60)
sns.despine()
plot3 = _.get_figure()
#plot3.savefig("Calls_Department.png")

#%%

days=['Monday','Tuesday','Wednesday','Thursday','Friday']

df_days = pd.DataFrame(index=days, columns=days)
callsbyday = [mon, tue, wed, thu, fri]
daily_calls = dict(zip(days, callsbyday))


for i in range(len(days)):
    for j in range(len(days)):
        res = stats.ttest_ind(daily_calls[days[i]], daily_calls[days[j]])
        df_days.iloc[i,j] = res[1]

p1_df = df_days.apply(pd.to_numeric)

d1 = p1_df.where(np.tril(np.ones(p1_df.shape)).astype(np.bool))
fig = sns.heatmap(d1, center = .05, cmap='coolwarm')
fig.set_title("P-Values from T-Test on Daily Call Volume Distributions")
plot = fig.get_figure()
#plot.savefig('Heatmap.png')