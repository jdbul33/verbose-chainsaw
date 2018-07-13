# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 12:43:26 2018

@author: jdbul
"""

from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.layouts import gridplot

#%%
"""
Create Pie Chart Bokeh visualization for total call time by dept
"""

from bokeh.transform import cumsum
from bokeh.palettes import Category20
from math import pi

df = pd.DataFrame(topics.groupby('KB_Article', as_index=False)['Seconds'].sum())
#df['Percentage'] = round(df['Seconds']/sum(df['Seconds']) *100, 2)
df = df.sort_values('Seconds', ascending=False)
others = pd.Series([df.iloc[9:,1].sum()])
others = pd.Series(['All Other Departments', others[0]], index=['KB_Article', 'Seconds'])
df = df.append(others, ignore_index=True)
df = df.drop(df.index[9:22])
df['Percentage'] = round(df['Seconds']/sum(df['Seconds']) *100, 2)
assert df.Percentage.sum() > 99.99 and df.Percentage.sum() < 100.01


df = df.set_index('KB_Article')
df['angle'] = df['Seconds']/sum(df['Seconds']) * 2*pi
df['color'] = Category20[len(df)]

output_file("Call_Time_Spent_Dept.html", title="Total Time Spent on Calls by Department \n 9/29/2016 - 06/15/2018")
p = figure(plot_height=400, title="Total Time Spent on Calls by Department \n 9/29/2016 - 06/15/2018", toolbar_location=None, tools="hover", tooltips="@KB_Article: @Percentage%")

p.wedge(x=0, y=1, radius=0.6, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'), line_color="white", fill_color='color',source=df)

p.axis.axis_label=None
p.axis.visible=False
p.grid.grid_line_color = None

#%%
"""
Create histogram of call durations by Department
This will be the new data
"""






#%%
"""
Create histogram of number of calls by day of the week
This can be done using daily data and topic data perhaps, for more complete 
"""






#%%
"""
Create a visualization of call durations by longest topics to resolve
This is going to be restricted to new topic data
"""





#%%
"""
Create a visualization of quickest topics to resolve by duration
New topic data as above
"""





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
