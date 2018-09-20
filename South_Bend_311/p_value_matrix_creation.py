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
plot = fig.get_figure()
#plot.savefig('Heatmap.png')


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
sns.set()

hist_dict = {}

for data, name in zip([mon, tue, wed, thu, fri], ['Monday','Tuesday','Wednesday','Thursday','Friday']):
    plt.figure()
    plt.title("Call Distribution for " + name)
    plt.xlabel("Number of Daily Calls")
    plt.ylabel("Number of Days")
    plt.xlim(0, 1200)
    plt.hist(data, bins=24)
    
#%%
import pylab
import matplotlib._pylab_helpers

figures=[manager.canvas.figure
         for manager in matplotlib._pylab_helpers.Gcf.get_all_fig_managers()]
print(figures)

plt.get_fignums():
