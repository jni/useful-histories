from scipy import sparse
import numpy as np
labels = np.array([[1, 1, 1, 2, 2],
                   [1, 1, 3, 2, 2],
                   [1, 3, 3, 3, 4]], int)
indices = np.arange(labels.size).reshape(labels.shape)
counts = np.bincount(labels.ravel())
ind_ptr = np.cumsum(counts)
indices = np.concatenate([np.flatnonzero(labels == i) for i in range(5)])
locs = sparse.csr_matrix((indices, indices, ind_ptr), dtype=int)
locs.todense().astype(int)
index_map = np.arange(labels.size).reshape(labels.shape)
locs[0].data
locs[1].data
ind_ptr2 = np.concatenate([[0], ind_ptr])
locs2 = sparse.csr_matrix((indices, indices, ind_ptr2), dtype=int)
locs2.todense()
