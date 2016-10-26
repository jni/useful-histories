# IPython log file


get_ipython().system('head Infected\\ 2-details.txt')
import pandas as pd
rbc = pd.read_csv('RBC1-details.txt', header=1, index_col=0)
rbc.shape
rbc = pd.read_csv('RBC1-details.txt', header=1, index_col=0, sep='\t')
rbc.shape
rbc.iloc[0]
rbc = pd.read_csv('RBC1-details.txt', header=0, index_col=0, sep='\t')
rbc.iloc[0]
import matplotlib.pyplot as plt
plt.scatter(rbc['Branch length'], rbc['Euclidean distance'])
rbc['squiggle'] = np.log2(rbc['Branch length'] / rbc['Euclidean distance'])
import numpy as np
rbc['squiggle'] = np.log2(rbc['Branch length'] / rbc['Euclidean distance'])
rbc.iloc[0]
np.all(rbc['V1 z'] == 0)
def clear_edges(skeldf):
    skeldf = skeldf[(skeldf['V1 x'] != 0) & (skeldf['V1 y' != 0]) &
                    (skeldf['V2 x'] != 0) & (skeldf['V2 y' != 0])]
    return skeldf
rbc1 = clear_edges(rbc)
def clear_edges(skeldf):
    skeldf = skeldf[(skeldf['V1 x'] != 0) & (skeldf['V1 y' != 0]) &
                    (skeldf['V2 x'] != 0) & (skeldf['V2 y' != 0]), :]
    return skeldf
rbc1 = clear_edges(rbc)
rbc[rbc['Skeleton ID'] == 2].shape
rbc.shape
rbc[(rbc['Skeleton ID'] == 2) & (rbc['V1 x'] == 0)].shape
def clear_edges(skeldf):
    skeldf = skeldf[(skeldf['V1 x'] != 0) & (skeldf['V1 y'] != 0) &
                    (skeldf['V2 x'] != 0) & (skeldf['V2 y'] != 0)]
    return skeldf
rbc1 = clear_edges(rbc)
rbc1.shape
def remove_cycles(skeldf):
    skeldf = skeldf[(skeldf['Euclidean distance'] == 0)]
    return skeldf
rbc2 = remove_cycles(rbc1)
rbc2.shape
(rbc['Euclidean distance'] > 0).sum()
(rbc1['Euclidean distance'] > 0).sum()
def remove_cycles(skeldf):
    skeldf = skeldf[(skeldf['Euclidean distance'] > 0)]
    return skeldf
rbc2 = remove_cycles(rbc1)
rbc2.shape
plt.scatter(rbc['Branch length'], rbc2['Euclidean distance'])
plt.scatter(rbc2['Branch length'], rbc2['Euclidean distance'])
plt.scatter(rbc2['Branch length'], rbc2['Euclidean distance'], c='red')
plt.figure()
get_ipython().magic('pinfo plt.hist')
import numpy as np
get_ipython().magic('pinfo np.histogram')
values, edges = np.histogram(rbc2['squiggle'], bins='auto')
centers = (edges[1:] + edges[:-1]) / 2
plt.plot(centers, values)
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
rbc4.shape
rbc3.shape
plt.scatter(rbc4['Branch length'], rbc4['Euclidean distance'], c='green')
import seaborn as sns
plt.figure()
sns.pairplot(rbc4[['Branch length', 'Euclidean distance', 'V1 x', 'V1 y']])
get_ipython().magic('ls ')
from skimage import io
rbcim = io.imread('RBC 1.tif')
rbcim.max()
rbc4['row1'] = rbc4['V1 y'] / 2.24826
rbc4.columns
np.median(np.abs(rbc4['row1'] - np.round(rbc4['row1])))
np.median(np.abs(rbc4['row1'] - np.round(rbc4['row1'])))
np.max(rbc4['row1'])
rbcim.shape
plt.figure(); plt.imshow(rbcim)
rbcim2 = 1 - rbcim / rbcim.max()
plt.figure(); plt.imshow(rbcim2)
plt.axis('off')
plt.tight_layout()
rbc4_short = rbc4[(rbc4['Euclidean distance'] < 25)]
rbc4_long = rbc4[(rbc4['Euclidean distance'] > 150)]
rbc4_mid = rbc4[(rbc4['Euclidean distance'] > 25) & (rbc4['Euclidean distance'] < 150)]
len(rbc4_mid) + len(rbc4_short) + len(rbc4_long) == len(rbc4)
sns.palettes.SEABORN_PALETTES
sns.palettes.color
get_ipython().magic('pinfo sns.palettes.color_palette')
sns.palettes.color_palette('colorblind', 3)
c1, c2, c3 = sns.palettes.color_palette('colorblind', 3)
get_ipython().magic('pinfo plt.Line2D')
rbc4['col1'] = rbc4['V1 x'] / 2.24826
rbc4['row2'] = rbc4['V2 y'] / 2.24826
rbc4['col2'] = rbc4['V2 x'] / 2.24826
rbc4_mid = rbc4[(rbc4['Euclidean distance'] > 25) & (rbc4['Euclidean distance'] < 150)]
rbc4_long = rbc4[(rbc4['Euclidean distance'] > 150)]
rbc4_short = rbc4[(rbc4['Euclidean distance'] < 25)]
for r, c, rr, cc in zip(rbc4_short[i] for i in ['row1', 'col1', 'row2', 'col2']):
    plt.Lines2D([c, cc], [r, rr], color=c1, marker=None)
    
for r, c, rr, cc in zip([rbc4_short[i] for i in ['row1', 'col1', 'row2', 'col2']]):
    plt.Lines2D([c, cc], [r, rr], color=c1, marker=None)
    
next(zip([rbc4_short[i] for i in ['row1', 'col1', 'row2'
, 'col2']])

)
next(zip([list(rbc4_short[i]) for i in ['row1', 'col1', 'row2', 'col2']]))
next(zip(*[list(rbc4_short[i]) for i in ['row1', 'col1', 'row2', 'col2']]))
for r, c, rr, cc in zip(*[list(rbc4_short[i]) for i in ['row1', 'col1', 'row2', 'col2']]):
    plt.Lines2D([c, cc], [r, rr], color=c1, marker=None)
    
for r, c, rr, cc in zip(*[list(rbc4_short[i]) for i in ['row1', 'col1', 'row2', 'col2']]):
    plt.Line2D([c, cc], [r, rr], color=c1, marker=None)
    
    
plt.figure(5)
for r, c, rr, cc in zip(*[list(rbc4_short[i]) for i in ['row1', 'col1', 'row2', 'col2']]):
    plt.Line2D([c, cc], [r, rr], color=c1, lw=2)
    
    
    
for r, c, rr, cc in zip(*[list(rbc4_short[i]) for i in ['row1', 'col1', 'row2', 'col2']]):
    plt.plot([c, cc], [r, rr], color=c1, marker=None)
    
for r, c, rr, cc in zip(*[list(rbc4_mid[i]) for i in ['row1', 'col1', 'row2', 'col2']]):
    plt.plot([c, cc], [r, rr], color=c2, marker=None)
    
    
for r, c, rr, cc in zip(*[list(rbc4_long[i]) for i in ['row1', 'col1', 'row2', 'col2']]):
    plt.plot([c, cc], [r, rr], color=c3, marker=None)
    
    
plt.imshow(rbcim2)
plt.axis(off)
plt.axes('off')
plt.axis('off')
rbc4['row1'].max()
rbcim3 = rbcim2[:1758]
from skimage import filters
from skimage import morphology
rbcim4 = filters.gaussian(rbcim3, sigma=3)
plt.imshow(rbcim4)
scale = 2.24826
rbcim_med = filters.median(rbcim4, morphology.disk(100 / scale))
rbcim_med.max()
rbcim4.max()
from skimage import img_as_ubyte, img_as_float
rbcim5 = img_as_ubyte(rbcim4) > rbcim_med
plt.imshow(rbcim5)
rbcim5[1355:1464, 138:202] = False
plt.imshow(rbcim5)
rbcim5[1355:1464, 138:202] = 0
plt.imshow(rbcim5)
rbcim5.max()
rbcim5.min()
plt.imshow(rbcim5, cmap='grey')
plt.imshow(rbcim5, cmap='gray')
plt.imshow(rbcim4, cmap='gray')
plt.imshow(rbcim4, cmap='gray_r')
plt.imshow(rbcim5, cmap='magma_r', alpha=0.5)
plt.imshow(rbcim4, cmap='gray')
plt.imshow(rbcim4, cmap='gray_r')
plt.imshow(rbcim5, cmap='viridis_r', alpha=0.3)
plt.rcParams['image.cmap']
plt.rcParams['image.cmap'] = 'gray'
rbcim5 = img_as_ubyte(rbcim4) < rbcim_med
plt.imshow(rbcim5)
plt.figure(); plt.imshow(rbcim4)
plt.figure(); plt.imshow(1 rbcim4)
plt.figure(); plt.imshow(1 - rbcim4)
plt.axis("off")
rbcim4 = 1 - rbcim4
get_ipython().set_next_input('rbcskel = morphology.skeletonize');get_ipython().magic('pinfo morphology.skeletonize')
rbcskel = morphology.skeletonize(rbcim5)
plt.imshow(1 - rbcim3)
plt.axis('off')
plt.imshow(np.dstack([rbcskel] * 4), cmap='red')
plt.imshow(np.dstack([rbcskel, np.zeros_like(rbcskel),]), cmap='red')
plt.imshow(np.dstack([rbcskel, np.zeros_like(rbcskel),
                      np.zeros_like(rbcskel), rbcskel]))
np.sum(rbcskel)
rbcskel_ids = np.zeros(rbcskel.shape, int)
rbcskel_ids[rbcskel] = np.arange(1, np.sum(rbcskel) + 1)
from skimage.future import graph
get_ipython().magic('pinfo graph.rag')
get_ipython().magic('pinfo graph.rag.RAG')
g = graph.RAG(rbcskel_ids, connectivity=2)
0 in g
g.remove_node(0)
g.number_of_nodes()
(1, 2) in g.edges()
(2, 1) in g.edges()
type(g)
super(g)
super(skimage.future.graph.rag.RAG, g)
import skimage
super(skimage.future.graph.rag.RAG, g)
super(skimage.future.graph.rag.RAG)
from scipy import ndimage
from scipy import ndimage as ndi
pix = np.ones((3, 3), dtype=bool)
pix.ravel()[pix.size//2] = 0
pix
ndi.distance_transform_edt(pix)
get_ipython().magic('pwd ')
get_ipython().magic('ls ')
import skeleton as skelpy
g = skelpy.skeleton_to_nx(rbcskel)
from imp import reload
reload(skelpy)
g = skelpy.skeleton_to_nx(rbcskel)
reload(skelpy)
g = skelpy.skeleton_to_nx(rbcskel)
reload(skelpy)
g = skelpy.skeleton_to_nx(rbcskel)
0 in g
reload(skelpy)
g = skelpy.skeleton_to_nx(rbcskel)
get_ipython().magic('pdb')
g = skelpy.skeleton_to_nx(rbcskel)
reload(skelpy)
g = skelpy.skeleton_to_nx(rbcskel)
reload(skelpy)
g = skelpy.skeleton_to_nx(rbcskel)
np.nonzero(rbcskel_int == 21991)
np.nonzero(rbcskelint == 21991)
np.nonzero(rbcskel_ids == 21991)
reload(skelpy)
g = skelpy.skeleton_to_nx(rbcskel)
g.number_of_nodes()
import itertools
itertools.count(i for i in g.nodes_iter() if g.node[i]['type'] == 'junction')
get_ipython().magic('pinfo itertools.count')
c = itertools.count()
import toolz as tz
get_ipython().magic('pinfo tz.count')
tz.count(i for i in g.nodes_iter() if g.node[i]['type'] == 'junction')
import networkx as nx
nx.shortest_path(45, 123)
get_ipython().magic('pinfo nx.shortest_path')
nx.shortest_path(g, 45, 123)
nx.shortest_path(g, 45, 150)
cc = max(nx.connected_component_subgraphs(g), key=len)
len(cc)
cc.nodes()[:10]
nx.shortest_path(cc, 1, 10)
nx.shortest_path_length(cc, 1, 10)
nx[1,2]
cc[1, 2]
cc[1][2]
cc[3][4]
cc.nodes()[-1]
nx.shortest_path_length(cc, 1, 144179)
get_ipython().magic('pinfo nx.shortest_path_length')
nx.shortest_path_length(cc, 1, 144179, weight='weight')
