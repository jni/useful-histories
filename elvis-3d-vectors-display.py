# IPython log file


import napari
viewer = napari.Viewer()
ch1, ch2 = viewer.layers[0], viewer.layers[1]
ch1.scale
get_ipython().run_line_magic('cd', '/Users/jni/data/elvis ')
get_ipython().system('head positionX.csv')
posx = np.loadtxt('positionX.csv', delimiter=',')
posx.shape
posx = np.loadtxt('positionX.csv', delimiter=',').reshape((193, 193, 22))
posx = np.loadtxt('positionY.csv', delimiter=',').reshape((193, 193, 22))
posx = np.loadtxt('positionX.csv', delimiter=',').reshape((193, 193, 22))
posy = np.loadtxt('positionY.csv', delimiter=',').reshape((193, 193, 22))
posz = np.loadtxt('positionZ.csv', delimiter=',').reshape((193, 193, 22))
vx1 = np.loadtxt('vx1.csv', delimiter=',').reshape((193, 193, 22))
vy1 = np.loadtxt('vy1.csv', delimiter=',').reshape((193, 193, 22))
vz1 = np.loadtxt('vz1.csv', delimiter=',').reshape((193, 193, 22))
get_ipython().run_line_magic('pinfo', 'viewer.add_vectors')
vectors = np.stack(
   [np.stack([posz.ravel(), posy.ravel(), posx.ravel()], axis=1),
    np.stack([vz1.ravel(), vy1.ravel(), vx1.ravel()], axis=1)],
   axis=2,
   ).transpose((0, 2, 1))
vectors.shape
vc_layer = viewer.add_vectors(vectors, scale=ch1.scale)
vectors_real = vectors[np.all(
    np.isfinite(vectors.reshape((vectors.shape[0], -1))),
    axis=1)]
vectors_real.shape
vc_layer = viewer.add_vectors(vectors, scale=ch1.scale)
get_ipython().run_line_magic('debug', '')
vc_layer = viewer.add_vectors(vectors[::100], scale=ch1.scale)
vc_layer = viewer.add_vectors(vectors_real[::100], scale=ch1.scale)
velocities = np.norm(vectors_real[:, 1, :], axis=1)
velocities = np.linalg.norm(vectors_real[:, 1, :], axis=1)
velocities.shape
plt.hist(velocities, bins='auto')
filter_vel = (velocities > 0) & (velocities < 0.04)
filter_vel = (velocities > 0) & (velocities < 0.004)
vc_layer2 = viewer.add_vectors(vectors_real[filter_vel][::100], scale=ch1.scale, length=1000, properties={'v': velocities[filter_vel]})
vc_layer2 = viewer.add_vectors(vectors_real[filter_vel][::100], scale=ch1.scale, length=1000, properties={'v': velocities[filter_vel][::100]})
import scipy.io
get_ipython().run_line_magic('pwd', '')
m = scipy.io.loadmat('/Users/jni/data/elvis/full\ data/VelocityMapCC3DCC_Image\ 4_Airyscan\ Processing_Subset2TOIsize10TOIShift3.mat')
m = scipy.io.loadmat('/Users/jni/data/elvis/full data/VelocityMapCC3DCC_Image 4_Airyscan Processing_Subset2TOIsize10TOIShift3.mat')
