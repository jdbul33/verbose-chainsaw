# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 20:18:38 2018

@author: jdbul
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


#%%
sns.set_style("white")
_ = sns.swarmplot(x='Day_of_Week', y='Total_Calls_Handled', data=daily_data)
_.set(xlabel="Day of the Week", ylabel="Number of Calls", xticklabels=['Mon','Tue','Wed','Thu','Fri'])
plt.show()


#%%

#%%

df = pd.DataFrame(topics.groupby('KB_Article', as_index=False)['Seconds'].sum())
#df['Percentage'] = round(df['Seconds']/sum(df['Seconds']) *100, 2)
df = df.sort_values('Seconds', ascending=False)
others = pd.Series([df.iloc[6:,1].sum()])
others = pd.Series(['Total Others', others[0]], index=['KB_Article', 'Seconds'])
df = df.append(others, ignore_index=True)
df = df.drop(df.index[6:23])
dept = list(df['KB_Article'])

for i in range(len(dept)):
    n = dept[i]
    dept[i] = n.replace(' - KB Team', '')
    
df['Department'] = dept

df['Total Call Time in Minutes'] = df['Seconds']//60    
#df = df.set_index('KB_Article')
#%%
sns.set_palette(sns.cubehelix_palette(7, start=2, rot=0, dark=.3, light=.65, reverse=True))

_ = sns.barplot(x='Department', y='Total Call Time in Minutes', data=df)
for item in _.get_xticklabels():
    item.set_rotation(60)
sns.despine()
_.set_title("Total Call Time by Department")
plot3 = _.get_figure()
#plot3.savefig("Calls_Department_sim.png")
