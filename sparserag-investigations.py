# IPython log file


from gala import agglo2, imio
frag = imio.read_image_stack('tests/example-data/train-ws.lzf.h5')
pr = imio.read_image_stack('tests/example-data/train-p1.lzf.h5')
g = agglo2.SparseRAG(frag, pr, [tz.identity, np.square])
g.graph[1, 2]
g.compute_feature_caches()
from importlib import reload
reload(agglo2)
g = agglo2.SparseRAG(frag, pr, [tz.identity, np.square])
g.compute_feature_caches()
g.compute_features(1, 2)
from gala import Rag
from gala import agglo
np.sum(pr[frag == 1])
np.sum(frag == 1)
np.sum(frag == 2)
np.mean(pr[frag == 1])
np.mean(np.square(pr)[frag == 1])
from gala import features
gorig = agglo.Rag(frag, pr, feature_manager=features.default.moments_hist())
mh = features.moments.moments_hist()
mh = features.default.moments_hist()
mh(gorig, 1, 2)
mm = features.moments.Manager()
get_ipython().set_next_input('mm = features.moments.Manager');get_ipython().magic('pinfo features.moments.Manager')
mm = features.moments.Manager(nmoments=2, use_diff_features=False)
gorig = agglo.Rag(frag, pr, feature_manager=mm)
mm(gorig, 1, 2)
g.compute_features(1, 2)
g.boundaries[g.graph[1, 2]].nonzero()
gorig.boundary(1, 2)
len(gorig.boundary(1, 2))
edges = g.graph.nonzero()
edges[0][:10], edges[1][:10]
g.boundaries[g.graph[1, 64]]
len(g.boundaries[g.graph[1, 64]])
len(gorig.boundary(1, 64))
get_ipython().magic('timeit g = agglo2.SparseRAG(frag, pr, [tz.identity, np.square])')
get_ipython().magic('timeit g.compute_features(1, 2)')
g.compute_features(1, 2)
get_ipython().magic('timeit mm(gorig, 1, 2)')
gorig = agglo.Rag(frag, pr, feature_manager=mm)
get_ipython().magic('timeit gorig = agglo.Rag(frag, pr, feature_manager=mm)')
get_ipython().magic('timeit gorig.compute_feature_caches()')
get_ipython().magic('timeit g.compute_feature_caches()')
frag0 = np.array([[1, 1, 1, 2, 2],
                  [1, 1, 1, 2, 2],
                  [3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3],
                  [3, 3, 3, 3, 3],
                  [4, 4, 5, 5, 5],
                  [4, 4, 5, 5, 5]])
                  
pr0 = np.array([[1, 0, 9, 8, 0],
                [9, 7, 9, 4, 3],
                [6, 7, 7, 3, 3],
                [0, 2, 0, 1, 1],
                [5, 4, 9, 8, 9],
                [3, 4, 9, 8, 8],
                [0, 7, 8, 3, 2]]) / 10
                
g0 = agglo2.SparseRAG(frag0, pr0, [tz.identity, np.square])
g0.graph.A
g.boundaries[1].A
g.boundaries[1]
g0.boundaries[1]
