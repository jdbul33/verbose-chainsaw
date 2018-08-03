# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 18:58:39 2018

@author: jdbul
"""
"""
Plots for paper, separate from dashboard plots
"""

import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row, column
from math import pi
from bokeh.transform import cumsum
from bokeh.palettes import Category20, brewer, Viridis, Magma, Category10
from bokeh.models import Jitter
from scipy.stats import sem

#%%
"""
Create Pie Chart Bokeh visualization for total call time by dept
"""


df = pd.DataFrame(topics.groupby('KB_Article', as_index=False)['Seconds'].sum())
#df['Percentage'] = round(df['Seconds']/sum(df['Seconds']) *100, 2)
df = df.sort_values('Seconds', ascending=False)
others = pd.Series([df.iloc[9:,1].sum()])
others = pd.Series(['All Other Departments', others[0]], index=['KB_Article', 'Seconds'])
df = df.append(others, ignore_index=True)
df = df.drop(df.index[9:22])
df['Percentage'] = round(df['Seconds']/sum(df['Seconds']) *100, 2)
assert df.Percentage.sum() > 99.99 and df.Percentage.sum() < 100.01
dept = list(df['KB_Article'])

for i in range(len(dept)):
    n = dept[i]
    dept[i] = n.replace(' - KB Team', '')
    
df['KB_Article'] = dept
    
df = df.set_index('KB_Article')
df['angle'] = df['Seconds']/sum(df['Seconds']) * 2*pi
df['color'] = Category20[len(df)]

p = figure(plot_height=400,x_range=(-1.5,3), title="Total Time Spent on Calls by Department \n 9/29/2016 - 06/15/2018", toolbar_location=None, tools="hover", tooltips="@KB_Article: @Percentage{0.0}%")
p.wedge(x=0, y=1, radius=1.2, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), line_color="white", fill_color='color', legend= "KB_Article", source=df)
p.axis.axis_label=None
p.axis.visible=False
p.grid.grid_line_color = None


#%%
"""
Create data visualization on a monthly basis
This will be the new data
maybe number, abandon, queue or something
"""

mon = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
call = []

for j in range(len(mon)):
    call.append(monthly_call_mean[monthly_call_mean['Month_of_Year']==mon[j]]['CallsPresented'])

cols = brewer['Set3'][12]

p3 = figure(x_axis_label='Month',
            y_axis_label="Mean Daily Number of Calls", x_range=mon, y_range=(0, 740))


p3.vbar(x=mon, top=call, width=0.7, fill_color=cols)

sem_month =[]
for i in range(len(mon)):
    sem_month.append(sem(daily_data[daily_data['Month_of_Year']==mon[i]]['CallsPresented']))


mon_top = [x+y for x,y in zip(call, sem_month)]
mon_bot = [x-y for x,y in zip(call, sem_month)]

p3.vbar(x=mon, top=mon_top, bottom=mon_bot, color='black', width=.05)
p3.xaxis.major_label_text_font_size = "12pt"
p3.yaxis.major_label_text_font_size = "12pt"
show(p3)








#%%
"""
Create histogram of number of calls by day of the week
This can be done using daily data and topic data perhaps, for more complete

daily data has a day of week
topic data does not 
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

acc_col = Category10[5]

p2 = figure(x_axis_label = 'Number of Calls per Day', title='Number of Calls by Day of Week 2013 - 2018; Click Legend to Hide/Show', background_fill_color = 'whitesmoke')

for data, name, color in zip([mon, tue, wed, thu, fri], ['Mon','Tue','Wed','Thu','Fri'], acc_col):
    hist, edges = np.histogram(data, density=True, bins=15)
    p2.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color=color, line_color="#033649", alpha=0.7, legend=name)

#hist, edges = np.histogram(mon, density=True, bins=15)            
#p2.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color=acc_col[0], line_color="#033649", alpha=0.6, legend='Mon')

#hist, edges = np.histogram(tue, density=True, bins=15)            
#p2.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color=acc_col[1], line_color="#033649", alpha=0.6, legend='Tue')
        
#hist, edges = np.histogram(wed, density=True, bins=15)            
#p2.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color=acc_col[2], line_color="#033649", alpha=0.6, legend='Wed')
        
#hist, edges = np.histogram(thu, density=True, bins=15)            
#p2.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color=acc_col[3], line_color="#033649", alpha=0.6, legend='Thu')
        
#hist, edges = np.histogram(fri, density=True, bins=15)            
#p2.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color=acc_col[4], line_color="#033649", alpha=0.6, legend='Fri')

p2.legend.location = "top_left"
p2.legend.click_policy="hide"


#%%
"""
Create a visualization of quickest topics to resolve by duration
New topic data as above

This is being limited to topics above 50% of the average call quantity.
This eliminates some of the one-off long call topics as outliers
"""
df_3 = topic_data[topic_data['Count'] >= .5*topic_data.Count.mean()]
df_3 = df_3.sort_values('Seconds', ascending=False)
quick_topics = list(df_3.iloc[-10:]['Topic'])
quick_times = list(df_3.iloc[-10:]['Seconds'])

sem_quick =[]
for t in range(len(quick_topics)):
    sem_quick.append(sem(topics[topics['Topic']==quick_topics[t]]['Seconds']))

quick_top = [x+y for x,y in zip(quick_times, sem_quick)]
quick_bot = [x-y for x,y in zip(quick_times, sem_quick)]

color = Viridis[len(quick_topics)]

p5 = figure(tools=['ypan','yzoom_out','reset'],x_range=quick_topics, y_range=(30,47), y_axis_label='Average Duration in Seconds', plot_height=400, title="Average Call Duration of Top 10 Quickest Topics; Adjusted Y-Axis")
p5.vbar(x=quick_topics, top=quick_times, width=0.6, fill_color=color, alpha=0.8)
p5.vbar(x=quick_topics, top=quick_top, bottom=quick_bot, color='black', width=.05)
p5.xaxis.major_label_orientation = pi/3

#%%
"""
Create a visualization of call durations by longest topics to resolve
This is going to be restricted to new topic data
"""
long_topics = list(df_3.iloc[0:10]['Topic'])
long_times = list(df_3.iloc[0:10]['Seconds'])

sem_long =[]
for t in range(len(long_topics)):
    sem_long.append(sem(topics[topics['Topic']==long_topics[t]]['Seconds']))

long_top = [x+y for x,y in zip(long_times, sem_long)]
long_bot = [x-y for x,y in zip(long_times, sem_long)]

color2 = Magma[len(long_times)]

p4 = figure(tools=['ypan','yzoom_out','reset','save'],x_range=long_topics, y_range=(175,245), y_axis_label='Average Duration in Seconds', plot_height=400, title="Average Call Duration of Top 10 Longest Topics; Adjusted Y-Axis")
p4.vbar(x=long_topics, top=long_times, width=0.6, fill_color=color2, alpha=0.8)
p4.vbar(x=long_topics, top=long_top, bottom=long_bot, color='black', width=.05)
p4.xaxis.major_label_orientation = pi/3

#%%
"""
use topic_data with jittering for the busiest departments to make a jitter 
plot, dept on x and call duration on y
"""
df_6 = topic_data

dept_name = list(df_6['KB_Article'])

for i in range(len(dept_name)):
    n = dept_name[i]
    dept_name[i] = n.replace(' - KB Team', '')
    
df_6['Dept'] = dept_name


df_6 = df_6.loc[(df_6['Dept'] == 'Water Works') |
        (df_6['Dept'] == 'Solid Waste') |
        (df_6['Dept'] == 'Streets') |
        (df_6['Dept'] == 'Code Enforcement') |
        (df_6['Dept'] == "Mayor's Office") |
        (df_6['Dept'] == 'Engineering') |
        (df_6['Dept'] == 'Animal Control')]

df_6.reset_index(drop=True, inplace=True)


colors = brewer['Set1'][7]
p6 = figure(title = 'Number of Calls by Topic for Busiest Departments (Misc. Trash Information Not to Scale)',
            y_range=(0,6200), tools=["hover", 'box_zoom', 'reset', 'save'], tooltips="@Topic; @Count calls")

for i, d in enumerate(list(df_6['Dept'].unique())):
    y = df_6[df_6['Dept'] == d][['Count', 'Topic']]
    color = colors[i  % len(colors)]
    p6.circle(x={'value': i, 'transform': Jitter(width=0.4)}, y='Count', source=y, color=color, size=10, alpha=0.75)

sw_trash = df_6[df_6['Topic'] == "Miscellaneous Trash Information"]
p6.diamond(x={'value': 1, 'transform': Jitter(width=0.4)}, y=5999, source=sw_trash, size=24, fill_color='red', line_color='blue', alpha=1)
labs = {}
for i in range(0,7):
    labs[i] = list(df_6['Dept'].unique())[i]

p6.xaxis.major_label_overrides = labs
p6.xaxis.major_label_orientation = pi/3
p6.xaxis.major_tick_line_color = None
p6.xaxis.minor_tick_line_color = None



