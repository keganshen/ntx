#!/usr/bin/env python
# coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame

pd.set_option('mpl_style','default')
data = {'90m':[3,5,5,],
        '1g':[90,130,140,],
        '3.4g':[1200,1200,1200],
       }
df = DataFrame(data,index=['d','w','m'],columns=['90m','1g','3.4g']).T


df.plot(kind='barh')
plt.legend(loc='best')
plt.savefig('plo1.png')
