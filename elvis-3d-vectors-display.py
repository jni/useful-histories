import os
import matplotlib.pyplot as plt
import napari
import numpy as np
import scipy.io


os.chdir('/Users/jni/data/elvis')

# load vector data
posx = np.loadtxt('positionX.csv', delimiter=',').ravel()
posx = np.loadtxt('positionY.csv', delimiter=',').ravel()
posx = np.loadtxt('positionX.csv', delimiter=',').ravel()
posy = np.loadtxt('positionY.csv', delimiter=',').ravel()
posz = np.loadtxt('positionZ.csv', delimiter=',').ravel()
vx1 = np.loadtxt('vx1.csv', delimiter=',').ravel()
vy1 = np.loadtxt('vy1.csv', delimiter=',').ravel()
vz1 = np.loadtxt('vz1.csv', delimiter=',').ravel()

# stack vectors to format (nvec, (pos, direction), ndim)
vectors = np.stack(
        [np.stack([posz, posy, posx], axis=1),
         np.stack([vz1, vy1, vx1], axis=1)],
        axis=2,
        ).transpose((0, 2, 1))

# subset to only vectors for which all entries are not nan/infinite
vectors_real = vectors[np.all(
        np.isfinite(vectors.reshape((vectors.shape[0], -1))),
        axis=1,
        )]

# compute velocities and to filter outliers
velocities = np.linalg.norm(vectors_real[:, 1, :], axis=1)
plt.hist(velocities, bins='auto')
plt.show()
filter_vel = (velocities > 0) & (velocities < 0.004)

# make a 3D viewer
viewer = napari.Viewer(ndisplay=3)

# load the image data
ch1, = viewer.open(
        'Image 4_Airyscan Processing_Subset2_t1_ch1.czi',
        plugin='napari-aicsimageio',
        )
ch2, = viewer.open(
        'Image 4_Airyscan Processing_Subset2_t1_ch2.czi',
        plugin='napari-aicsimageio',
        )

# add the vectors data, subsampling to ever 100th vector
# Note: vector positions and velocities are in pixel space
# Note: vectors are in a tiny scale so scale length by 1000
vc_layer = viewer.add_vectors(
        vectors_real[filter_vel][::100],
        scale=ch1.scale,
        length=1000,
        properties={'v': velocities[filter_vel][::100]},
        )

# show the viewer
napari.run()

# For future reference: load the full .mat data
m = scipy.io.loadmat('/Users/jni/data/elvis/full data/VelocityMapCC3DCC_Image 4_Airyscan Processing_Subset2TOIsize10TOIShift3.mat')
