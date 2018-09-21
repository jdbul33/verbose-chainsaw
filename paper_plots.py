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