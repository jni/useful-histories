# IPython log file


import dask.array as d
import dask.array as da
lls = da.from_zarr('data/gokul-lls/aollsm-m4-560nm.zarr')
lls = da.from_zarr('gokul-lls/aollsm-m4-560nm.zarr')
lls2 = da.from_zarr('gokul-lls/aollsm-m4-560nm-downscale.zarr')
import napari
v = napari.view_image([lls, lls2], is_pyramid=True,
    contrast_limits=[0, 150000])
