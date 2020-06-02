# IPython log file


from skimage import graph
image = np.array([[1, 1, 2, 2], [2, 1, 1, 3], [3, 2, 1, 2], [2, 2, 2, 1]])
mcp = graph.MCP_Geometric(image)
destinations = [[0, 0], [3, 3]]
costs, traceback = mcp.find_costs(destinations)
type(traceback)
print(traceback)
graph.
mcp.traceback
get_ipython().run_line_magic('pinfo', 'mcp.traceback')
mcp.traceback([0, 0])
mcp.traceback([0, 3])
mcp.offsets
mcp
from skimage.graph import _mcp
offsets = _mcp.make_offsets(2, True)
offsets
traceback
indices = np.indices(traceback.shape)
offsets.append([0, 0])
indices.shape
offsets_arr = np.array(offsets)
offsets_arr.shape
offset_to_neighbor = offsets_arr[traceback]
offset_to_neighbor.shape
neighbor_index = indices + offset_to_neighbor.transpose((2, 0, 1))
neighbor_index = indices - offset_to_neighbor.transpose((2, 0, 1))
get_ipython().run_line_magic('pinfo', 'np.ravel_multi_index')
ids = np.arange(traceback.size).reshape(image.shape)
neighbor_ids = np.ravel_multi_index(tuple(neighbor_index), traceback.shape)
ids
neighbor_ids
from scipy import sparse
g = sparse.coo_matrix((ids.ravel(), neighbor_ids.ravel(), np.ones(traceback.size))).to_csr()
get_ipython().run_line_magic('pinfo', 'sparse.coo_matrix')
g = sparse.coo_matrix((np.ones(traceback.size), (ids.ravel(), neighbor_ids.ravel()))).to_csr()
g = sparse.coo_matrix((np.ones(traceback.size), (ids.ravel(), neighbor_ids.ravel()))).tocsr()
get_ipython().run_line_magic('pinfo', 'sparse.csgraph.connected_components')
sparse.csgraph.connected_components(g)[1].reshape((4, 4))
neighbor_ids
ids
print(indices.shape)
print(ids)
print(neighbor_ids)
print _39
print(_39)
print(costs)
g2 = sparse.coo_matrix((np.ones(traceback.size), (ids.flat, neighbor_ids.flat))).tocsr()
g2.shape
sparse.csgraph.connected_components(g2)[1].reshape((4, 4))
