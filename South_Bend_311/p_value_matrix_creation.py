# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 22:19:19 2018

@author: jdbul
"""

import pandas as pd
import numpy as np
from scipy import stats

month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

calls = []
for i in range(len(month)):
    mon = daily_data.loc[daily_data['Month_of_Year'] == month[i]]
    calls.append(list(mon.CallsPresented.values))

monthly_calls = dict(zip(month, calls))

p_df = pd.DataFrame(index=month, columns=month)

for i in range(len(month)):
    for j in range(len(month)):
        
    



jul_mar_ttest = stats.ttest_ind(jul_calls, mar_calls)

