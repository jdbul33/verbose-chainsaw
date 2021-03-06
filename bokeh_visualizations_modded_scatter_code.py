# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 12:43:26 2018

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
"""
 

mon = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
call = []

for j in range(len(mon)):
    call.append(monthly_call_mean[monthly_call_mean['Month_of_Year']==mon[j]]['CallsPresented'])

cols = brewer['Set3'][12]

p3 = figure(title='Average Daily Call Volume by Month, 2013-2015', x_axis_label='Month',
            y_axis_label="Mean Daily Number of Calls", x_range=mon, y_range=(0, 740))


p3.vbar(x=mon, top=call, width=0.7, fill_color=cols)

sem_month =[]
for i in range(len(mon)):
    sem_month.append(sem(daily_data[daily_data['Month_of_Year']==mon[i]]['CallsPresented']))


mon_top = [x+y for x,y in zip(call, sem_month)]
mon_bot = [x-y for x,y in zip(call, sem_month)]


source_error = ColumnDataSource(data=dict(base=mon, lower=mon_bot, upper=mon_top))


p3.add_layout(Whisker(source=source_error, base='base', upper='upper', lower='lower', level='overlay'))

p3.xaxis.major_label_text_font_size = "11pt"
p3.yaxis.major_label_text_font_size = "11pt"







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

p2 = figure(x_axis_label = 'Number of Calls per Day', y_axis_label = 'Number of Days',title='Number of Calls by Day of Week 2013 - 2018; Click Legend to Hide/Show', background_fill_color = 'whitesmoke')

for data, name, color in zip([mon, tue, wed, thu, fri], ['Mon','Tue','Wed','Thu','Fri'], acc_col):
    hist, edges = np.histogram(data, bins=8)
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
p2.xaxis.major_label_text_font_size = "11pt"
p2.yaxis.major_label_text_font_size = "11pt"
p2.yaxis.formatter = NumeralTickFormatter(format="0,0")


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

source_error1 = ColumnDataSource(data=dict(base=quick_topics, lower=quick_bot, upper=quick_top))

color = Viridis[len(quick_topics)]

p5 = figure(tools=['ypan','yzoom_out','reset', 'save'],x_range=quick_topics, y_range=(30,47), y_axis_label='Average Duration in Seconds', plot_height=400, title="Average Call Duration of Top 10 Quickest Topics; Adjusted Y-Axis")
p5.vbar(x=quick_topics, top=quick_times, width=0.6, fill_color=color, alpha=0.8)
p5.add_layout(Whisker(source=source_error1, base='base', upper='upper', lower='lower', level='overlay'))


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


source_error2 = ColumnDataSource(data=dict(base=long_topics, lower=long_bot, upper=long_top))

color2 = Magma[len(long_times)]

p4 = figure(tools=['ypan','yzoom_out','reset','save'],x_range=long_topics, y_range=(175,245), y_axis_label='Average Duration in Seconds', plot_height=400, title="Average Call Duration of Top 10 Longest Topics; Adjusted Y-Axis")
p4.vbar(x=long_topics, top=long_times, width=0.6, fill_color=color2, alpha=0.8)
p4.add_layout(Whisker(source=source_error2, base='base', upper='upper', lower='lower', level='overlay'))
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
p6.xaxis.major_label_text_font_size = "11pt"
p6.yaxis.major_label_text_font_size = "11pt"


#%%
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

colors = Viridis[7]
p8 = figure(title = 'Average Duration and Number of Calls by Topic in Top Departments \n 9/2016 - 6/2018', x_axis_label = "Average Duration in Seconds", 
            y_axis_label = 'Total Number of Calls by Topic',
             tools=["hover",'box_zoom', 'reset', 'save'], tooltips="@Topic; average duration of @Seconds seconds; @Count total calls")

for i, d in enumerate(list(df_6['Dept'].unique())):
    y = df_6[df_6['Dept'] == d][['Count', 'Seconds', 'Topic']]
    color = colors[i  % len(colors)]
    if d == 'Water Works':
        p8.circle(x='Seconds', y='Count', source=y, color=color, size=12, alpha=0.75, legend= d)
    elif d == 'Solid Waste':
        p8.diamond(x='Seconds', y='Count', source=y, color=color, size=12, alpha=0.75, legend= d)
    elif d == 'Streets':
        p8.triangle(x='Seconds', y='Count', source=y, color=color, size=12, alpha=0.75, legend= d)
    elif d == 'Code Enforcement':
        p8.square(x='Seconds', y='Count', source=y, color=color, size=12, alpha=0.75, legend= d)
    elif d == "Mayor's Office":
        p8.inverted_triangle(x='Seconds', y='Count', source=y, color=color, size=12, alpha=0.75, legend= d)
    elif d == 'Engineering':
        p8.x(x='Seconds', y='Count', source=y, color=color, size=12, alpha=0.75, legend= d)
    elif d == 'Animal Control':
        p8.cross(x='Seconds', y='Count', source=y, color=color, size=12, alpha=0.75, legend= d)
   

p8.diamond(x=75, y=4000, size=24, fill_color='red', line_color='blue', alpha=1)
p8.xaxis.major_label_orientation = pi/3
p8.xaxis.major_tick_line_color = None
p8.xaxis.minor_tick_line_color = None
p8.xaxis.major_label_text_font_size = "11pt"
p8.yaxis.major_label_text_font_size = "11pt"

p8.legend.location = "top_right"
p8.legend.click_policy="hide"

#%%
"""
Adding y slider
"""

callback = CustomJS(args=dict(yr=p8.y_range), code="""

// JavaScript code goes here

var a = cb_obj.value[0];

// the model that triggered the callback is cb_obj:
var b = cb_obj.value[1];

// models passed as args are automagically available
yr.start = a;
yr.end = b;

""")
    
y_range_slider = RangeSlider(start=0, end=4200, value=(0,4200), step=20, title="Zoom by Number of Total Calls",
                              callback_policy='mouseup')


y_range_slider.js_on_change('value', callback) 




#%%
"""
Adding x slider
"""

callback = CustomJS(args=dict(xr=p8.x_range), code="""

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

show(row(p8, widgetbox(y_range_slider, x_slider)))





#%%
"""
Create a gridplot layout and a shareable HTML file
This will effectively be a dashboard that will be interactive
"""


g = row(p, p2)
h = row(p4, p5)
j = row(p6, p3)
k = row(p8, widgetbox(y_range_slider, x_slider))
output_file('CallCenterDashboard.html', title='311 Call Center Dashboard')
show(column(g,h,j,k))

