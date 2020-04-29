# IPython log file


arr = np.random.random((64,) * 3)
plt.imshow(arr)
from skimage import data
get_ipython().run_line_magic('pinfo', 'data.binary_blobs')
from skimage.util import random_noise
get_ipython().run_line_magic('pinfo', 'random_noise')
blobs_raw = np.stack([data.binary_blobs(length=64, ndim=3, blob_size_fraction=0.05, volume_fraction=f)
                      for f in np.linspace(0.05, 0.5, 10)])
blobs_raw = np.stack([data.binary_blobs(length=64, n_dim=3, blob_size_fraction=0.05, volume_fraction=f)
                      for f in np.linspace(0.05, 0.5, 10)])
blobs_sp = random_noise(blobs_raw, mode='s&p')
blobs = random_noise(blobs_sp, mode='poisson')
import napari
napari.view_image(blobs)
blobs_raw = np.stack([data.binary_blobs(length=64, n_dim=3, blob_size_fraction=0.1, volume_fraction=f)
                      for f in np.linspace(0.05, 0.5, 10)])
blobs_sp = random_noise(blobs_raw, mode='s&p')
blobs_g = random_noise(blobs_sp, mode='gaussian')
blobs = random_noise(blobs_g, mode='poisson')
napari.view_image(blobs)
plt.imshow(blobs[5, 32])
napari.view_image(blobs)
napari.view_image(blobs)
from skimage import morphology
blobs_clean = morphology.closing(morphology.opening(blobs))
viewer = napari.view_image(blobs, blending='additive', colormap='cyan')
viewer.add_image(blobs_clean, blending='additive', colormap='magenta')
100000 * 200000 / 1e9
get_ipython().run_line_magic('pinfo', 'random_noise')
get_ipython().run_line_magic('pinfo', 'ndi.generate_binary_structure')
get_ipython().run_line_magic('pinfo', 'ndi.grey_opening')
get_ipython().run_line_magic('pinfo', 'ndi.label')
viewer = napari.view_image(blobs, blending='additive', colormap='cyan')
import numpy as np
import toolz as tz
from skimage import data, util


blobs_raw = np.stack([
    data.binary_blobs(length=64, n_dim=3, blob_size_fraction=0.05,
                      volume_fraction=f)
    for f in np.linspace(0.05, 0.5, 10)
])

add_noise = tz.curry(util.random_noise)
blobs = tz.pipe(
    blobs_raw,
    add_noise(mode='s&p'),
    add_noise(mode='gaussian'),
    add_noise(mode='poisson')
)
viewer = napari.view_image(blobs, name='blobs')
get_ipython().run_line_magic('pinfo', 'data.binary_blobs')
import numpy as np
import toolz as tz
from skimage import data, util


blobs_raw = np.stack([
    data.binary_blobs(length=64, n_dim=3, volume_fraction=f)
    for f in np.linspace(0.05, 0.5, 10)
])

add_noise = tz.curry(util.random_noise)
blobs = tz.pipe(
    blobs_raw,
    add_noise(mode='s&p'),
    add_noise(mode='gaussian'),
    add_noise(mode='poisson')
)
viewer = napari.view_image(blobs, name='blobs')
from scipy import ndimage as ndi

neighbors3d = ndi.generate_binary_structure(3, connectivity=1)
neighbors = neighbors3d[np.newaxis, ...]

opening, closing = map(tz.curry, [ndi.grey_opening, ndi.grey_closing])

denoised = tz.pipe(
    blobs,
    opening(footprint=neighbors),
    closing(footprint=neighbors)
)
denoised_layer = viewer.add_image(denoised, name='denoised')
blobs_layer = viewer.layers['blobs']
blobs_layer.blending = 'additive'
blobs_layer.colormap = 'magenta'
denoised_layer.blending = 'additive'
denoised_layer.colormap = 'cyan'
from skimage import filters

binary = filters.threshold_li(denoised) < denoised
labels = ndi.label(binary, structure=neighbors)

labels_layer = viewer.add_labels(labels, name='labeled', opacity=0.7)
neighbors.sahpe
neighbors.shape
binary.shape
from skimage import filters

neighbors2 = np.concatenate(
    (np.zeros_like(neighbors), neighbors, np.zeros_like(neighbors))
)

binary = filters.threshold_li(denoised) < denoised
labels = ndi.label(binary, structure=neighbors2)[0]

labels_layer = viewer.add_labels(labels, name='labeled', opacity=0.7)
get_ipython().run_line_magic('pinfo', 'measure.marching_cubes_lewiner')
get_ipython().run_line_magic('pinfo', 'measure.marching_cubes_lewiner')
meshes = [measure.marching_cubes_lewiner(b.astype(float), level=0.5) for b in binary]
len(meshes)
vertices = np.concatenate(
    [np.hstack(np.full(len(v), i), v) for i, (v, _, _, _) in enumerate(meshes)], axis=0
)
vertices = np.concatenate(
    [np.hstack((np.full(len(v), i), v)) for i, (v, _, _, _) in enumerate(meshes)], axis=0
)
type(meshes[0])
type(meshes[0][0])
[v.shape for v, _, _, _ in meshes]
vertices = np.concatenate(
    [np.vstack((np.full(len(v), i), v)) for i, (v, _, _, _) in enumerate(meshes)], axis=0
)
vertices = np.concatenate(
    [np.concatenate((np.full((len(v), 1), i), v), axis=1) for i, (v, _, _, _) in enumerate(meshes)], axis=0
)
vert_lens = list(map(len, (m[0] for m in meshes)))
index_offset = [0] + list(np.cumsum(vert_lens)[:-1])
faces = np.concatenate(
    [f[i] + off for (_, f, _, _), off in zip(meshes, index_offset)],
    axis=0
)
faces = np.concatenate(
    [f + off for (_, f, _, _), off in zip(meshes, index_offset)],
    axis=0
)
len(verts)
len(vertices)
np.max(faces, axis=0)
values = ndi.map_coordinates(vertices.T, labels, order=0)
vertices.shape
labels.shape
vertices.T.shape[0]
labels.ndim
values = ndi.map_coordinates(labels, vertices.T, order=0)
values.dtype
surface = viewer.add_surface((vertices, faces, values))
meshes = [measure.marching_cubes_lewiner(b.astype(float), level=0.8) for b in binary]
vertices = np.concatenate(
    [np.concatenate((np.full((len(v), 1), i), v), axis=1) for i, (v, _, _, _) in enumerate(meshes)], axis=0
)
faces = np.concatenate(
    [f + off for (_, f, _, _), off in zip(meshes, index_offset)],
    axis=0
)
values = ndi.map_coordinates(labels, vertices.T, order=0)
surface = viewer.add_surface((vertices, faces, values))
vert_lens = list(map(len, (m[0] for m in meshes)))
index_offset = [0] + list(np.cumsum(vert_lens)[:-1])
faces = np.concatenate(
    [f + off for (_, f, _, _), off in zip(meshes, index_offset)],
    axis=0
)
surface = viewer.add_surface((vertices, faces, values))
