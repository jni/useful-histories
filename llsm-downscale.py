# IPython log file
from tqdm import tqdm
import numpy as np
import dask.array as da
import zarr
import itertools
from skimage.transform import downscale_local_mean


lls = da.from_zarr('gokul-lls/aollsm-m4-560nm.zarr')
lls3 = zarr.open(
    'gokul-lls/aollsm-m4-560nm-downscale.zarr',
    dtype=np.float32,
    shape=(199, 201, 192, 256),
    chunks=(1, 201, 192, 256),
)
indices = list(itertools.product(range(199), range(201)))
for i, j in tqdm(indices):
    lls3[i, j] = downscale_local_mean(np.array(lls[i, j]), (4, 4))

