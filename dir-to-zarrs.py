# IPython log file


from glob import glob
import json
import toolz as tz
from aicsimageio import imread, metadata, AICSImage
import pathlib
import zarr
import tifffile

g = glob('**/.zarray', root_dir='.', recursive=True)
get_chunks = lambda fn: tz.pipe(fn, open, json.load, tz.curried.get('chunks'), tuple)
all_chunks = set(map(get_chunks, g))
# get_ipython().system('mkdir /Users/jni/Dropbox/data/finding-and-following')
get_shape = (
        lambda fn: tz.pipe(fn, open, json.load, tz.curried.get('shape'), tuple)
        )
all_shapes = set(map(get_shape, g))
root = pathlib.Path('.')
im = imread('tracking/human_exvivo/201118_hTR4_DMSO_3000s_.nd2')

zim = np.asarray(zarr.open('segmentation/invivo_example/ground_truth/medium - control/saline_example_GT_PL.zarr'))
zim.shape

# We use a different "imread" function depending on the file format
map_open = {
        'tif': tifffile.imread,
        'zarr': lambda fn: np.asarray(zarr.open(fn)),
        'nd2': imread,
        }
images = [p for p in root.rglob('*')
          if str(p).endswith(('zarr', 'nd2', 'tif', 'tiff'))]
new_root = pathlib.Path('/Users/jni/Dropbox/data/finding-and-following/')

# some useful pathlib.Path methods:
# p = images[0]
# set(f.suffix for f in images)
# p.name
# p.root
# p.parts

for im in images:
    suffix = im.suffix[1:]
    read_fn = map_open[suffix]
    arr = read_fn(im)
    prefix = (1,) * (arr.ndim - 3)
    out_fn = (
            new_root / im.parent / str(im.name)[:-len(im.suffix)]
            ).with_suffix('.zarr')
    out_zarr = zarr.open(
            out_fn,
            shape=arr.shape,
            chunks=prefix + (12, 128, 128),
            dtype=arr.dtype,
            mode='w',
            )
    out_zarr[:] = arr

