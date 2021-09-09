# IPython log file

import napari
import numpy as np
from skimage import feature

arr0 = np.asarray(da.from_zarr('Pia/Large and dense finished/train_TR67_Inj7_fr112_PL.zarr'))
arr1 = np.asarray(da.from_zarr('Volga/Large and Dense DONE/train_TR67_Inj7_fr112.zarr'))
coords0 = pd.DataFrame(measure.regionprops_table(arr0, properties=('centroid',))).to_numpy()
coords1 = pd.DataFrame(measure.regionprops_table(arr1, properties=('centroid',))).to_numpy()
viewer = napari.Viewer()
viewer.open('/home/jni/Dropbox/data/Deep learning training/Large and Dense/train_TR67_Inj7_fr112.nd2')
matches = feature.match_descriptors(coords0, coords1)
matches0 = np.zeros(len(coords0), dtype=bool)
matches1 = np.zeros(len(coords1), dtype=bool)
matches0[matches[:, 0]] = True
matches1[matches[:, 1]] = True
colorcycle0 = [(0.0, 0.0, 0.0, 0.0), (1.0, 1.0, 0.0, 1.0)]
colorcycle1 = [(0.0, 0.0, 0.0, 0.0), (0.0, 1.0, 1.0, 1.0)]
viewer.add_points(coords0, name='pia', edge_color='white', size=np.where(matches0, 1, 3), face_color=matches0, face_color_cycle=colorcycle0, scale=viewer.layers[0].scale)
