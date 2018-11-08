# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 11:25:39 2018

@author: jdbul
"""

import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row, column, widgetbox
from math import pi
from bokeh.transform import cumsum
from bokeh.palettes import Category20, brewer, Viridis, Magma, Category10
from bokeh.models import Jitter, Whisker, ColumnDataSource, NumeralTickFormatter
from scipy.stats import sem
from bokeh.models.widgets import RangeSlider
from bokeh.models.callbacks import CustomJS

#%%
"""
retooling Jitterplot code to make scatter plot with sliders, clickable legend, etc
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

df_6 = df_6.drop(df_6[df_6.Count < 20].index)

df_6.reset_index(drop=True, inplace=True)

#df_6.sort_values(by='Count', ascending=False, inplace=True)

colors = brewer['Set1'][7]
p6 = figure(title = 'Average Duration and Number of Calls by Topic in Top Departments \n 9/2016 - 6/2018', x_axis_label = "Average Duration in Seconds", 
            y_axis_label = 'Total Number of Calls by Topic',
             tools=["hover", 'reset', 'save'], tooltips="@Topic; average duration of @Seconds seconds; @Count total calls")

for i, d in enumerate(list(df_6['Dept'].unique())):
    y = df_6[df_6['Dept'] == d][['Count', 'Seconds', 'Topic']]
    color = colors[i  % len(colors)]
    if d == 'Water Works':
        p6.circle(x='Seconds', y='Count', source=y, color=color, size=12, alpha=0.75, legend= d)
    elif d == 'Solid Waste':
        p6.diamond(x='Seconds', y='Count', source=y, color=color, size=12, alpha=0.75, legend= d)
    elif d == 'Streets':
        p6.triangle(x='Seconds', y='Count', source=y, color=color, size=12, alpha=0.75, legend= d)
    elif d == 'Code Enforcement':
        p6.square(x='Seconds', y='Count', source=y, color=color, size=12, alpha=0.75, legend= d)
    elif d == "Mayor's Office":
        p6.inverted_triangle(x='Seconds', y='Count', source=y, color=color, size=12, alpha=0.75, legend= d)
    elif d == 'Engineering':
        p6.x(x='Seconds', y='Count', source=y, color=color, size=12, alpha=0.75, legend= d)
    elif d == 'Animal Control':
        p6.circle_cross(x='Seconds', y='Count', source=y, color=color, size=12, alpha=0.75, legend= d)
   

p6.xaxis.major_label_orientation = pi/3
p6.xaxis.major_tick_line_color = None
p6.xaxis.minor_tick_line_color = None
p6.xaxis.major_label_text_font_size = "11pt"
p6.yaxis.major_label_text_font_size = "11pt"

p6.legend.location = "top_right"
p6.legend.click_policy="hide"


#%%
"""
Adding y slider
"""

callback = CustomJS(args=dict(yr=p6.y_range), code="""

// JavaScript code goes here

var a = cb_obj.value[0];

// the model that triggered the callback is cb_obj:
var b = cb_obj.value[1];

// models passed as args are automagically available
yr.start = a;
yr.end = b;

""")
    
y_range_slider = RangeSlider(start=0, end=13000, value=(0,13000), step=20, title="Zoom by Number of Total Calls",
                              callback_policy='mouseup')


y_range_slider.js_on_change('value', callback) 




#%%
"""
Adding x slider
"""

callback = CustomJS(args=dict(xr=p6.x_range), code="""

// JavaScript code goes here

var a = cb_obj.value[0];

// the model that triggered the callback is cb_obj:
var b = cb_obj.value[1];

// models passed as args are automagically available
xr.start = a;
xr.end = b;

""")
    
x_slider = RangeSlider(start=0, end=400, value=(0,400), step=10, title="Zoom by Average Call Duration",
                        callback_policy='mouseup')


x_slider.js_on_change('value', callback) 

#p6.x_range.js_on_change('start', callback)
   


show(row(p6, widgetbox(y_range_slider, x_slider)))
