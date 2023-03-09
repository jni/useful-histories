# IPython log file

import ome_zarr
from ont import imreads
from ome_zarr.io import parse_url
from ome_zarr.writer import write_multiscale
from ome_zarr.writer import write_multiscales_metadata
import zarr

# imdir load_images reads nested directories of image files into dask ndarray
arr = imreads('01', '*.tif')
# trim edges so each axis is divisible by 4
arr_mid = arr[:, 2:-1, 2:-1, :-1]

# like numpy.mean, but maintains dtype
def mean_dtype(arr, **kwargs):
    return np.mean(arr, **kwargs).astype(arr.dtype)

# chunk; high-res chunks are optimized for 2D viewing without compromising 3D
# too much. Remaining chunks are optimized for 3D.
# TODO: what is the dask-optimized way to do this? would be much more efficient
# to process all scales of each time point, but couldn't figure out an elegant
# way to do this.
scale0 = arr_mid.rechunk((1, 64, 512, 512))
scale1 = da.coarsen(
        mean_dtype, scale0, {1: 2, 2: 2, 3: 2}
        ).rechunk((1, 256, 256, 256))
scale2 = da.coarsen(
        mean_dtype, scale0, {1: 4, 2: 4, 3: 4}
        ).rechunk((1, 256, 256, 256))

# OME-NGFF v0.4 parameter definitions; should probably hardcode that spec
# number in the code 😅
coordtfs = [
        [{'type': 'scale', 'scale': [90, 0.38, 0.38, 0.38]},
         {'type': 'translation', 'translation': [0, 0, 0, 0]}],
        [{'type': 'scale', 'scale': [90, 0.74, 0.74, 0.74]},
         {'type': 'translation', 'translation': [0, 0.19, 0.19, 0.19]}],
        [{'type': 'scale', 'scale': [90, 1.48, 1.48, 1.48]},
         {'type': 'translation', 'translation': [0, 0.95, 0.95, 0.95]}],
        ]
axes = [{'name': 't', 'type': 'time', 'unit': 'second'},
        {'name': 'z', 'type': 'space', 'unit': 'micrometer'},
        {'name': 'y', 'type': 'space', 'unit': 'micrometer'},
        {'name': 'x', 'type': 'space', 'unit': 'micrometer'}]

# Open the zarr group manually
path = '01.ome.zarr'
store = parse_url(path, mode='w').store
root = zarr.group(store=store)

# Use OME write multiscale; this actually computes the dask arrays but does so
# in a memory-efficient way. ❤️ 🚀
write_multiscale([scale0, scale1, scale2],
        group=root, axes=axes, coordinate_transformations=coordtfs
        )

# if the metadata writing failed, you can recover:
# datasets = [
#         {'path': str(i), 'coordinateTransformations': coordtfs[i]}
#         for i in range(len(coordtfs))
#         ]
# write_multiscales_metadata(root, datasets=datasets, axes=axes)

# add omero metadata: the napari ome-zarr plugin uses this to pass rendering
# options to napari.
root.attrs['omero'] = {
        'channels': [{
                'color': 'ffffff',
                'window': {'start': 400, 'end': 6000},
                'label': 'tribolium',
                'active': True,
                }]
        }
