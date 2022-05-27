# IPython log file

import os

import dask.array as da
import napari
import numpy as np
import pandas as pd
from skimage import feature, measure

datadir = os.path.expanduser('~/Dropbox/data/Deep learning training')

arr0 = np.asarray(
    da.from_zarr(
        os.path.join(
            datadir,
            'Proofread files/Pia/Large and dense finished/'
            'train_TR67_Inj7_fr112_PL.zarr',
        )
    )
)
arr1 = np.asarray(
    da.from_zarr(
        os.path.join(
            datadir,
            'Proofread files/Volga/Large and Dense DONE/'
            'train_TR67_Inj7_fr112.zarr',
        )
    )
)
coords0 = pd.DataFrame(
    measure.regionprops_table(arr0, properties=('centroid',))
).to_numpy()
coords1 = pd.DataFrame(
    measure.regionprops_table(arr1, properties=('centroid',))
).to_numpy()

matches = feature.match_descriptors(coords0, coords1)
matches0 = np.zeros(len(coords0), dtype=bool)
matches1 = np.zeros(len(coords1), dtype=bool)
matches0[matches[:, 0]] = True
matches1[matches[:, 1]] = True
colorcycle0 = ['black', 'yellow']
colorcycle1 = ['black', 'cyan']

viewer = napari.Viewer()
viewer.open(os.path.join(datadir, 'Large and Dense/train_TR67_Inj7_fr112.nd2'))
viewer.add_points(
    coords0,
    name='pia',
    edge_color='white',
    size=np.where(matches0, 1, 3),
    symbol='ring',
    face_color={
        'colors': 'matched',
        'categorical_colormap': {True: 'black', False: 'yellow'},
        'mode': 'cycle',
    },
    scale=viewer.layers[0].scale,
    properties={'matched': matches0},
)
viewer.add_points(
    coords1,
    name='volga',
    edge_color='white',
    size=np.where(matches1, 1, 3),
    symbol='ring',
    face_color={
        'colors': 'matched',
        'categorical_colormap': {True: 'black', False: 'cyan'},
        'mode': 'cycle',
    },
    scale=viewer.layers[0].scale,
    properties={'matched': matches1},
)

napari.run()
