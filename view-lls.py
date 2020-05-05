# IPython log file
import os
import sys
import dask.array as da
import napari
from napari.utils import resize_dask_cache

if sys.platform == 'linux':
    media = '/media/jni'
elif sys.platform == 'darwin':
    media = '/Volumes'

lls = da.from_zarr(
    os.path.join(media, 'datac/napari-data/gokul-lls/aollsm-m4-560nm.zarr')
)
lls2 = da.from_zarr(
    os.path.join(
        media, 'datac/napari-data/gokul-lls/aollsm-m4-560nm-downscale.zarr'
    )
)

with napari.gui_qt():
    v = napari.view_image(
        lls_560nm := [lls, lls2],
        multiscale=True,
        contrast_limits=[0, 150000],
        scale=(1, 3, 1, 1),
    )
    resize_dask_cache(200e6)
