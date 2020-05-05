# IPython log file
from tqdm import tqdm
import numpy as np
import dask.array as da
import zarr
import itertools
from skimage.transform import downscale_local_mean


lls3 = zarr.open(
    'gokul-lls/aollsm-m4-560nm-downscale.zarr',
    dtype=np.float32,
    shape=(199, 201, 192, 256),
    chunks=(1, 201, 192, 256),
)
lls4 = zarr.open(
    'gokul-lls/aollsm-m4-560nm-downscale2.zarr',
    dtype=np.float32,
    shape=(199, 100, 96, 128),
    chunks=(1, 100, 96, 128),
)
indices = list(range(199))
for i in tqdm(indices):
    lls4[i] = downscale_local_mean(np.array(lls3[i, :200]), (2, 2, 2))

