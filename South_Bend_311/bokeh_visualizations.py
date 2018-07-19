# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 12:43:26 2018

@author: jdbul
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show
#from bokeh.io import output_file, show
from bokeh.layouts import gridplot, row, column
from math import pi
from bokeh.transform import cumsum
from bokeh.palettes import Category20, Category10, Inferno, Category20c, brewer
from bokeh.models import CategoricalColorMapper, Jitter
#from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs
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

p = figure(plot_height=400, title="Total Time Spent on Calls by Department \n 9/29/2016 - 06/15/2018", toolbar_location=None, tools="hover", tooltips="@KB_Article: @Percentage{0.0}%")
p.wedge(x=0, y=1, radius=0.6, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), line_color="white", fill_color='color',source=df)
p.axis.axis_label=None
p.axis.visible=False
p.grid.grid_line_color = None

#%%
"""
Create histogram of call durations by Department
This will be the new data
"""


df_2 = topics
dept_to_filter = list(df_2['KB_Article'].unique())
dept_to_filter.sort()

for i in range(len(dept_to_filter)):
    n = dept_to_filter[i]
    dept_to_filter[i] = n.replace(' - KB Team', '')








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



acc_col = brewer['Dark2'][5]

p2 = figure(x_axis_label = 'Number of Calls per Day', title='Number of Calls by Day of Week 2013 - 2018', background_fill_color = 'ivory')

for data, name, color in zip([mon, tue, wed, thu, fri], ['Mon','Tue','Wed','Thu','Fri'], acc_col):
    hist, edges = np.histogram(data, density=True, bins=15)
    p2.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color=color, line_color="#033649", alpha=0.6, legend=name)

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


color = Category10[len(quick_topics)]

p5 = figure(x_range=quick_topics, y_axis_label='Average Duration in Seconds', plot_height=400,tools="hover", tooltips="Average Call Duration: @top{0.0} seconds", title="Average Call Duration of Top 10 Quickest Topics")
p5.vbar(x=quick_topics, top=quick_times, width=0.9, fill_color=color)
p5.xaxis.major_label_orientation = pi/3


#%%
"""
Create a visualization of call durations by longest topics to resolve
This is going to be restricted to new topic data
"""
long_topics = list(df_3.iloc[0:10]['Topic'])
long_times = list(df_3.iloc[0:10]['Seconds'])


color2 = Inferno[len(long_times)]

p4 = figure(x_range=long_topics, y_axis_label='Average Duration in Seconds', plot_height=400,tools="hover", tooltips="Average Call Duration: @top{0.0} seconds", title="Average Call Duration of Top 10 Longest Topics")
p4.vbar(x=long_topics, top=long_times, width=0.9, fill_color=color2)
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
p6 = figure(title = 'Number of Calls by Topic for Busiest Departments',
            y_range=(0,600), tools="hover", tooltips="@Topic")

for i, d in enumerate(list(df_6['Dept'].unique())):
    y = df_6[df_6['Dept'] == d][['Count', 'Topic']]
    color = colors[i  % len(colors)]
    p6.circle(x={'value': i, 'transform': Jitter(width=0.4)}, y=y['Count'], color=color)

labs = {}
for i in range(0,7):
    labs[i] = list(df_6['Dept'].unique())[i]

p6.xaxis.major_label_overrides = labs
p6.xaxis.major_label_orientation = pi/3
p6.xaxis.major_tick_line_color = None
p6.xaxis.minor_tick_line_color = None
show(p6)
# need to add hover tool for topics and figure out scaling issue

#%%
"""
Create a gridplot layout and a shareable HTML file
This will effectively be a crude dashboard that will be interactive
"""
output_file('311_Call_Center_Dashboard.html', title='311 Call Center Dashboard')

g = row(p, p2)
h = row(p4, p5)

show(column(g,h))
output_file('311_Call_Center_Dashboard.html', title='311 Call Center Dashboard')
