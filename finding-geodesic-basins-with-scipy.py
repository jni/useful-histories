# IPython log file
# See https://stackoverflow.com/questions/62135639/mcp-geometrics-for-calculating-marketsheds/62144556
import numpy as np
from scipy import sparse
from skimage import graph
from skimage.graph import _mcp


image = np.array([[1, 1, 2, 2], [2, 1, 1, 3], [3, 2, 1, 2], [2, 2, 2, 1]])
mcp = graph.MCP_Geometric(image)
destinations = [[0, 0], [3, 3]]
costs, traceback = mcp.find_costs(destinations)
offsets = _mcp.make_offsets(2, True)
indices = np.indices(traceback.shape)
offsets.append([0, 0])
offsets_arr = np.array(offsets)
offset_to_neighbor = offsets_arr[traceback]
neighbor_index = indices - offset_to_neighbor.transpose((2, 0, 1))
ids = np.arange(traceback.size).reshape(image.shape)
neighbor_ids = np.ravel_multi_index(tuple(neighbor_index), traceback.shape)
g = sparse.coo_matrix((
    np.ones(traceback.size),
    (ids.flat, neighbor_ids.flat),
)).tocsr()
basins = sparse.csgraph.connected_components(g)[1].reshape((4, 4))
print(basins)
