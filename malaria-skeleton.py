# IPython log file
import os
import matplotlib.pyplot as plt
import pandas as pd
import re  # regular expressions, for text matching
import seaborn.apionly as sns

data = pd.read_excel('/Users/jni/Dropbox/data1/malaria/adam-oli-schizont-30sec-output/skeleton.xlsx')

def infection_status(filename):
    if 'Uninf' in filename:
        return 'normal'
    else:
        return 'infected'
    
data['infection'] = data['filename'].apply(infection_status)

def cell_number(filename):
    regex = r'.*RBC(\d+)_\d\d.tif'
    regex = re.compile(regex)
    match = regex.match(filename)
    if match is not None:
        return int(match.group(1))
    else:
        return None
    
def field_number(filename):
    regex = r'.*RBC\d+_(\d\d).tif'
    regex = re.compile(regex)
    match = regex.match(filename)
    if match is not None:
        return int(match.group(1))
    else:
        return None
    
data['cell number'] = data['filename'].apply(cell_number)
data['field number'] = data['filename'].apply(field_number)

# save the full data with additional columns
directory = '/Users/jni/Dropbox/data1/malaria/adam-oli-schizont-30sec-output'
data.to_hdf(os.path.join(directory, 'skeleton-preprocess.hdf'), key='pre0')

# subset the data to only have specific shape index and branch type
ridges = ((data['mean shape index'] < 0.625) &
          (data['mean shape index'] > 0.125))
j2j = data['branch-type'] == 2
datar = data.loc[ridges & j2j]

# Plot the full dataset boxplot
sns.boxplot(data=datar, x='infection', y='branch-distance')
plt.show(block=True)

# Plot the boxplot of the image means
## First, group by filename and compute the means
means = datar.groupby('filename').mean().reset_index()
## This deletes non-numeric columns so we need to add them back
means['infection'] = means['filename'].apply(infection_status)
sns.boxplot(data=means, x='infection', y='branch-distance')
plt.show(block=True)

# plot the boxplot of the cell means
cellmeans = datar.groupby(('infection', 'cell number')).mean().reset_index()
sns.boxplot(x='infection', y='branch-distance', hue='cell number', data=cellmeans)
plt.show(block=True)
