# IPython log file
import numpy as np
import dask.array as da
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix

from skan import csr, draw
from matplotlib.patches import Circle

fig, ax = plt.subplots()
b = np.asarray(da.from_zarr('sample.zarr'))
image = np.zeros_like(b, dtype=float)
image[0, 0] = 1  # just need a black background
skel = csr.Skeleton(b, source_image=image)
draw.overlay_skeleton_2d_class(
        skel,
        image_cmap='gray',
        axes=ax,
        vmin=0,
        skeleton_colormap='viridis_r'
        )
center = np.array([54, 57])
radii = np.arange(3, 42, 3)
circles = [Circle((57, 54), radius=r, fill=False, edgecolor='cornflowerblue')
           for r in radii]
for c in circles:
    ax.add_patch(c)
    
edges = skel.graph.tocoo()
coords0 = skel.coordinates[edges.row]
coords1 = skel.coordinates[edges.col]
d0 = distance_matrix(coords0, [center]).ravel()
d1 = distance_matrix(coords1, [center]).ravel()
bins0 = np.digitize(d0, radii)
bins1 = np.digitize(d1, radii)
crossings = bins0 != bins1
shells = np.minimum(bins0[crossings], bins1[crossings])
print(radii)
print(np.bincount(shells) / 2)

plt.show()
