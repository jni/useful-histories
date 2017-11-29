# IPython log file


x = np.array([[0.0, 1.5, 2.7],
              [1.5, 0.0, 0.0],
              [2.7, 0.0, 0.0]])
              
y = sparse.csr_matrix(x)
y
import networkx as nx
g = nx.from_scipy_sparse_matrix(y)
g[0][1]
get_ipython().run_line_magic('cd', '~/Dropbox/data1/drosophila-embryo/')
get_ipython().run_line_magic('ls', '')
from gala import imio
v = imio.read_h5_stack('embA_0.3um_Probabilities.h5')
np.prod(v[..., 0]) * 8
np.prod(v[..., 0].shape) * 8
np.prod(v[..., 0].shape) * 8 / 1.9
np.prod(v[..., 0].shape) * 8 / 1e9
np.prod(v[..., 0].shape) * 2 / 1e9
v.shape
smoothed_vm = filters.gaussian(v[..., 0], sigma=4)
h = plt.hist(smoothed_vm.ravel(), bins='auto');
from fast_histogram import histogram1d as hist
values = hist(smoothed_vm.ravel(), bins=255)
values = hist(smoothed_vm.ravel(), range=[0, 1], bins=255)
plt.plot(values)
np.max(smoothed_vm)
b = smoothed_vm > 0.5
get_ipython().run_line_magic('pwd', '')
sys.path.append('/Users/jni/projects/mpl-volume-viewer/')
import slice_view as sv
view = sv.SliceViewer(b)
np.bincount(ndi.label(v).ravel())
np.bincount(ndi.label(b).ravel())
np.bincount(ndi.label(b)[0].ravel())
b2 = morphology.remove_small_objects(b, 10000)
sys.path.append('/Users/jni/projects/skan')
sys.path.append('/Users/jni/projects/unfold-embryo')
import unfold
g, idxs, path = unfold.define_mesoderm_axis(b2, spacing=0.3)
reload(unfold)
g, idxs, path = unfold.define_mesoderm_axis(b2, spacing=0.3)
get_ipython().run_line_magic('debug', '')
reload(unfold)
g, idxs, path = unfold.define_mesoderm_axis(b2, spacing=0.3)
np.max(idxs)
np.shape(g)
np.shape(idxs)
idxs[0]
idxs[3396]
np.max(path)
bflat = np.max(b2, axis=0)
plt.imshow(bflat)
idxs_path = idxs[:, 1:3][path]
plt.plot(idxs_path[:, 1], idxs_path[:, 0])
len(path)
values = [4.9, 3.0, 99.1]
values = np.array(values)
values[[[0, 0, 1],
        [2, 1, 1],
        [2, 2, 1]]]
        
indices = np.array([[0, 0, 1], [2, 1, 1], [2, 2, 1]])
values[indices]
idxs_path_smoothed = ndi.gaussian_filter(idxs_path, sigma=(10, 0), mode='reflect')
plt.plot(idxs_path_smoothed[:, 1], idxs_path_smoothed[:, 0])
idxs_path_smoothed = ndi.gaussian_filter(idxs_path, sigma=(50, 0), mode='reflect')
plt.plot(idxs_path_smoothed[:, 1], idxs_path_smoothed[:, 0])
get_ipython().run_line_magic('pinfo', 'ndi.gaussian_filter')
idxs_path_smoothed = ndi.gaussian_filter(idxs_path, sigma=(50, 0), mode='nearest')
plt.plot(idxs_path[:, 1], idxs_path[:, 0])
plt.plot(idxs_path_smoothed[:, 1], idxs_path_smoothed[:, 0])
