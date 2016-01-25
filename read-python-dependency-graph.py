# IPython log file


import itertools as it
with open('pypi-deps.txt', 'r') as fin:
    lines = fin.readlines()
    edges = [line.rstrip().split() for line in lines]
    packages = set(list(it.chain(*edges)))
    
len(edges)
len(packages)
'skimage' in packages
import toolz as tz
from toolz import curried as c
dep_count = tz.pipe(edges, c.pluck(1), tz.frequencies)
dep_count['skimage']
import networkx as nx
deps = nx.DiGraph()
'scikit-image' in packages
'scikit-learn' in packages
for u, v in edges:
    u = u.replace('scikit-', 'sk')
    v = v.replace('scikit-', 'sk')
    deps.add_edge(u, v)
    
deps.number_of_edges()
deps.number_of_nodes()
deps.node['skimage']
deps.in_edges('skimage')
nodes = nx.katz_centrality(deps)
central = sorted(deps.nodes(), key=nodes.__getitem__, reverse=True)
central[:10]
central[:20]
central[:40]
central[40:80]
central.index('skimage')
central.index('scipy')
import pickle
stdlib = pickle.load(open('/Users/jni/projects/depsy/data/python_standard_libs.pickle', 'rb'))
central_nonstd = list(tz.filter(lambda x: x not in stdlib, central))
len(central_nonstd)
central_nonstd.index('scipy')
len(central)
central[:5]
nx.is_connected(deps.to_undirected())
len(packages)
deps_sym = deps.to_undirected()
import numpy as np
conncomps = list(nx.connected_component_subgraphs(deps_sym))
giant = conncomps[0]
giant_d = deps.subgraph(giant.nodes())
gpackages = giant_d.nodes()
A = nx.to_scipy_sparse_matrix(giant_d)
A.shape
A.dtype
n = A.shape[0]
c = (A + A.T) / 2
c.dtype
from scipy import sparse
d = sparse.diags([np.asarray(c.sum(axis=0)).ravel()], [0])
L = d.tocsr() - c
b = (c.multiply((A - A.T).sign())).sum(axis=1)
type(b)
