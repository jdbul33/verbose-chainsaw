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
plot.savefig('Heatmap.png')
