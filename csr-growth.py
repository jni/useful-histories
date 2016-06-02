# IPython log file


import pickle
with open('sim-results.pickle', 'rb') as fin:
    s = pickle.load(fin)
    
len(s)
next(s.keys())
next(iter(s.keys()))
plt.plot(s[(160000, 0.2, 0)])
from matplotlib import pyplot as plt
plt.plot(s[(160000, 0.2, 0)])
plt.plot(np.cumsum(s[(160000, 0.2, 0)]))
import numpy as np
plt.plot(np.cumsum(s[(160000, 0.2, 0)]))
worst = (160000, 0.2)
worst_loads = [s[worst + (rep,)] for rep in range(5)]
worst_total = [np.cumsum(load)[-1] for load in worst_loads]
worst_total
np.mean(worst_total)
np.std(worst_total)
def multiplier(loads):
    return 2 * np.sum(loads) / len(loads)

import pandas as pd
df_source = [[nrow, q, np.sum(load), np.sum(load) / nrow]
             for (nrow, q, i), load in s.items()]
get_ipython().set_next_input('data = pd.DataFrame');get_ipython().magic('pinfo pd.DataFrame')
data = pd.DataFrame(df_source, columns=['nrows', 'q', 'total size', 'load factor'])
data.plot.scatter(x='nrows', y='total size', c='q')
data.plot.hist('load factor', c='q')
data['load factor'].plot.hist(by=data['q'])
from matplotlib import pyplot as plt
plt.show()
data['load factor'].plot.hist(by=data['q'])
get_ipython().set_next_input("data['load factor'].plot.hist");get_ipython().magic('pinfo plot.hist')
get_ipython().magic('pinfo data.plot.hist')
np.unique(data['q'])
get_ipython().magic('pinfo np.unique')
data['qint'] = np.unique(data['q'], return_inverse=True)[1]
data['load factor'].plot.hist(by=data['qint'])
data['load factor'].plot.hist(by=data['qint'], bins=100)
get_ipython().magic('pinfo plt.hist')
type(data['load factor'] - 2)
type(np.log(data['load factor'] - 2))
(np.log(data['load factor'] - 2)).plot.hist(bins=100)
(np.log(data['load factor'] - 2)).plot.hist(bins=100)
np.log(np.unique(data['q']))
np.diff(np.log(np.unique(data['q'])))
np.log(np.unique(data['q'])) + 2
type(data.groupby('q'))
np.log(data.groupby('q')).mean()
np.log(data.groupby('q')['load factor'] - 2).mean()
data['log added load'] = np.log(data['load factor'] - 2)
data.groupby('q')['log added load'].mean()
data.groupby('q')['log added load'].mean().diff()
data.groupby('q')['log added load'].std()
