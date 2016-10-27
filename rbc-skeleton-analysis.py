import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['image.cmap'] = 'gray'
import seaborn as sns
from skimage import io
from skimage import filters
from skimage import morphology
from skimage import img_as_ubyte, img_as_float
from scipy import ndimage as ndi

rbc = pd.read_csv('RBC1-details.txt', header=0, index_col=0, sep='\t')

plt.figure(1)
plt.scatter(rbc['Branch length'], rbc['Euclidean distance'])
rbc['squiggle'] = np.log2(rbc['Branch length'] / rbc['Euclidean distance'])

def clear_edges(skeldf):
    skeldf = skeldf[(skeldf['V1 x'] != 0) & (skeldf['V1 y'] != 0) &
                    (skeldf['V2 x'] != 0) & (skeldf['V2 y'] != 0)]
    return skeldf

rbc1 = clear_edges(rbc)

def remove_cycles(skeldf):
    skeldf = skeldf[(skeldf['Euclidean distance'] > 0)]
    return skeldf

rbc2 = remove_cycles(rbc1)
plt.figure(1)
plt.scatter(rbc2['Branch length'], rbc2['Euclidean distance'], c='red')

values, edges = np.histogram(rbc2['squiggle'], bins='auto')
centers = (edges[1:] + edges[:-1]) / 2
plt.figure(); plt.plot(centers, values)

def normal_squiggle(skeldf, low=0.015, high=0.3):
    squiggle = np.log2(skeldf['Branch length'] /
                       skeldf['Euclidean distance'])
    out = skeldf[(squiggle > low) & (squiggle < high)]
    return out

rbc3 = normal_squiggle(rbc2)

plt.figure(1)
plt.scatter(rbc3['Branch length'], rbc3['Euclidean distance'], c='cyan')

def select_skel(skeldf, skelid):
    out = skeldf[(skeldf['Skeleton ID'] == skelid)]
    return out

rbc4 = select_skel(rbc3, 2)
plt.figure(1)
plt.scatter(rbc4['Branch length'], rbc4['Euclidean distance'], c='green')

sns.pairplot(rbc4[['Branch length', 'Euclidean distance', 'V1 x', 'V1 y']])

rbcim = io.imread('RBC 1.tif')
rbcim2 = rbcim / rbcim.max()

scale = 2.24826  # pixel spacing in nm
rbc4['row1'] = rbc4['V1 y'] / scale
rbc4['col1'] = rbc4['V1 x'] / scale
rbc4['row2'] = rbc4['V2 y'] / scale
rbc4['col2'] = rbc4['V2 x'] / scale
rbc4_mid = rbc4[(rbc4['Euclidean distance'] > 25) & (rbc4['Euclidean distance'] < 150)]
rbc4_long = rbc4[(rbc4['Euclidean distance'] > 150)]
rbc4_short = rbc4[(rbc4['Euclidean distance'] < 25)]

plt.figure()
plt.imshow(rbcim2)
plt.axis('off')
plt.tight_layout()

c1, c2, c3 = sns.palettes.color_palette('colorblind', 3)

for r, c, rr, cc in zip(*[list(rbc4_short[i]) for i in ['row1', 'col1', 'row2', 'col2']]):
    plt.plot([c, cc], [r, rr], color=c1, marker=None)
    
for r, c, rr, cc in zip(*[list(rbc4_mid[i]) for i in ['row1', 'col1', 'row2', 'col2']]):
    plt.plot([c, cc], [r, rr], color=c2, marker=None)
    
    
for r, c, rr, cc in zip(*[list(rbc4_long[i]) for i in ['row1', 'col1', 'row2', 'col2']]):
    plt.plot([c, cc], [r, rr], color=c3, marker=None)
    
rbcim3 = rbcim2[:1758]
rbcim4 = filters.gaussian(rbcim3, sigma=3)
rbcim_med = filters.median(rbcim4, morphology.disk(100 / scale))
rbcim5 = img_as_ubyte(rbcim4) > rbcim_med
rbcskel = morphology.skeletonize(rbcim5)
rbcskel_ids = np.zeros(rbcskel.shape, int)
rbcskel_ids[rbcskel] = np.arange(1, np.sum(rbcskel) + 1)

import skeleton as skelpy
import networkx as nx
import toolz as tz
g = skelpy.skeleton_to_nx(rbcskel)
g.number_of_nodes()
tz.count(i for i in g.nodes_iter() if g.node[i]['type'] == 'junction')
cc = max(nx.connected_component_subgraphs(g), key=len)
n0, n1 = cc.nodes()[0], cc.nodes()[-1]
print(nx.shortest_path_length(cc, n0, n1, weight='weight'))
