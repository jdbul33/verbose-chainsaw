# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 21:24:28 2018

@author: jdbul

This is the script to make a Q-Q plot.  It will run after the primary call analysis
script
"""


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import percentileofscore

#%%
"""
"""

df = pd.read_csv('final_groups.csv')
df.drop(columns = ['Percentage'], inplace=True)

#%%


df['Call_Percentile'] = np.nan
df['Duration_Percentile'] = np.nan

call_vol_list = list(df['Count'])
call_dur_list = list(df['Seconds'])

for i in range(len(df)):
    x = df['Count'].iloc[i]
    y = df['Seconds'].iloc[i]
    df['Call_Percentile'][i] = percentileofscore(call_vol_list, x)
    df['Duration_Percentile'][i] = percentileofscore(call_dur_list, y)







#%%

from matplotlib.ticker import PercentFormatter
plt.figure()


_ = sns.regplot(x=df['Call_Percentile'], y=df['Duration_Percentile'], fit_reg=False)
sns.despine()
_.set_title('Percentile Plot of Topics, Call Volume by Call Duration')
_.set_xlabel('Total Call Volume Percentile')
_.set_ylabel('Total Call Duration Percentile')


_.yaxis.set_major_formatter(PercentFormatter())

_.xaxis.set_major_formatter(PercentFormatter())
