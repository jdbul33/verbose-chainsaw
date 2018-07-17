# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 12:43:26 2018

@author: jdbul
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.layouts import gridplot, row, column
from math import pi
#%%
"""
Create Pie Chart Bokeh visualization for total call time by dept
"""

from bokeh.transform import cumsum
from bokeh.palettes import Category20


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

output_file("Call_Time_Spent_Dept.html", title="Total Time Spent on Calls by Department \n 9/29/2016 - 06/15/2018")
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
from bokeh.palettes import Category20c
from bokeh.models import CategoricalColorMapper, ColumnDataSource
from bokeh.models.widgets import CheckboxGroup, Slider, RangeSlider, Tabs
from bokeh.layouts import WidgetBox

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
"""










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

from bokeh.palettes import Category10
color = Category10[len(quick_topics)]

p5 = figure(x_range=quick_topics, plot_height=400,tools="hover", tooltips="Average Call Duration: @top{0.0} seconds", title="Average Call Duration of Top 10 Quickest Topics")
p5.vbar(x=quick_topics, top=quick_times, width=0.9, fill_color=color)
p5.xaxis.major_label_orientation = pi/3


#%%
"""
Create a visualization of call durations by longest topics to resolve
This is going to be restricted to new topic data
"""
long_topics = list(df_3.iloc[0:10]['Topic'])
long_times = list(df_3.iloc[0:10]['Seconds'])

from bokeh.palettes import Inferno
color2 = Inferno[len(long_times)]

p4 = figure(x_range=long_topics, y_axis_label='Average Duration in Seconds', plot_height=400,tools="hover", tooltips="Average Call Duration: @top{0.0} seconds", title="Average Call Duration of Top 10 Longest Topics")
p4.vbar(x=long_topics, top=long_times, width=0.9, fill_color=color2)
p4.xaxis.major_label_orientation = pi/3


#%%
"""
Call Volume by hour throughout each day of the week
This will be a wide, flowing line chart showing call volume in 15 min. increments
This could be a combo of new and old case data
need to add day of week to old data
"""







#%%
"""
Create a gridplot layout and a shareable HTML file
This will effectively be a crude dashboard that will be interactive
"""
g = gridplot()

output_file('311_Call_Center_Dashboard.png', title='311 Call Center Dashboard')
show(g)