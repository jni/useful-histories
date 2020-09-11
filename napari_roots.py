from pathlib import Path

import dask
from dask import array as da
import imageio as iio
import napari
from skimage.io.collection import alphanumeric_key


def read_root_images(path):
    """Return a dask array correctly stacking the root images."""
    path = Path(path)
    subdirectories = [p for p in path.iterdir() if p.is_dir()]
    first_volume = [p for p in subdirectories[0].iterdir() if p.suffix == '.cb']
    single_file = first_volume[0]
    nvolumes = len(subdirectories)
    nz = len(first_volume)
    image0 = iio.imread(single_file)
    file_shape = image0.shape
    file_dtype = image0.dtype
    time_vol = da.stack(
        [
            da.stack(
                [da.from_delayed(
                    dask.delayed(iio.imread)(fn.as_posix()),
                    shape=file_shape,
                    dtype=file_dtype
                )
                for fn in [p for p in subdir.iterdir() if p.suffix == '.cb']
                ]
            )
            for subdir in subdirectories
        ]
    )
    return time_vol