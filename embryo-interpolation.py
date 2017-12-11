# IPython log file


image = np.zeros((2048, 2048), dtype=float)
image[0, 0] = 1
np.percentile(image, [0.1, 99.9])
get_ipython().run_line_magic('pinfo', 'np.percentile')
np.stack([np.zeros((3, 2)), np.zeros(3)], axis=1)
from skimage import data
image = data.horse().astype(bool)
plt.imshow(image)
get_ipython().run_line_magic('timeit', 'ndi.distance_transform_edt(~image, return_distances=False,')
get_ipython().run_line_magic('timeit', 'ndi.distance_transform_edt(~image, return_distances=False, return_indices=True)')
x = ndi.distance_transform_edt(~image, return_distances=False, return_indices=True)
x.shape
image_src = np.arange(image.size).reshape(image)
image_src = np.arange(image.size).reshape(image.shape)
image_src[~image] = 0
ws = segmentation.watershed(image, image_src, compactness=1e10)
get_ipython().run_line_magic('timeit', 'segmentation.watershed(image, image_src, compactness=1e10)')
import sys
sys.path.append('/Users/jni/projects/unfold-embryo')
from gala import imio
v = imio.read_h5_stack('embA_0.3um_Probabilities.h5')
get_ipython().run_line_magic('cd', '~/Dropbox/data1/drosophila-embryo/')
v = imio.read_h5_stack('embA_0.3um_Probabilities.h5')
v.shape
v0 = v[..., 0]
smoothed_vm = filters.gaussian(v[..., 0], sigma=4)
b = smoothed_vm > 0.5
b2 = morphology.remove_small_objects(b, 10000)
sys.path.append('/Users/jni/projects/skan')
import unfold
g, idxs, path = unfold.define_mesoderm_axis(b2)
sources, ids, idxs = unfold.source_id_volume(b2, idxs, path)
c0 = unfold.coord0_volume(sources, idxs)
c1 = unfold.coord1_volume(b2)
get_ipython().run_line_magic('ls', '')
image = io.imread('embA_0.3um.tif')
image.shape
channels = [unfold.sample2d(c0, c1, image[..., c])
            for c in range(3)]
            
reload(unfold)
channels = [unfold.sample2d(c0, c1, image[..., c])
            for c in range(3)]
            
