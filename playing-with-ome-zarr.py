# IPython log file


from glob import glob
get_ipython().run_line_magic('pinfo', 'glob')
g = glob('.zarray', root_dir='.', recursive=True)
len(g)
g = glob('**/.zarray', root_dir='.', recursive=True)
len(g)
import json
import toolz as tz
get_chunks = lambda fn: tz.pipe(fn, open, json.load, tz.pluck('chunks'))
all_chunks = set(map(get_chunks, g))
get_chunks = lambda fn: tz.pipe(fn, open, json.load, tz.curried.pluck('chunks'))
all_chunks = set(map(get_chunks, g))
all_chunks
type(g)
all_chunks = set(list(map(get_chunks, g)))
all_chunks
get_chunks(g[0])
json.load(open(g[0]))
tz.pluck('chunks', json.load(open(g[0])))
get_ipython().run_line_magic('pinfo', 'tz.pluck')
tz.get('chunks', json.load(open(g[0])))
get_chunks = lambda fn: tz.pipe(fn, open, json.load, tz.curried.get('chunks'))
all_chunks = set(map(get_chunks, g))
get_chunks = lambda fn: tz.pipe(fn, open, json.load, tz.curried.get('chunks'), tuple)
all_chunks = set(map(get_chunks, g))
all_chunks
get_ipython().system('mkdir /Users/jni/Dropbox/data/finding-and-following')
get_shape = lambda fn: tz.pipe(fn, open, json.load, tz.curried.get('shape'), tuple)
all_shapes = set(map(get_shape, g))
all_shapes
12 * 128 * 128
12 * 128 * 128 * 16 / 1e6
from aicsimageio import imread, metadata, AICSImage
im = imread('tracking/human_exvivo/201118_hTR4_DMSO_3000s_.nd2')
im = imread('tracking/human_exvivo/201118_hTR4_DMSO_3000s_.nd2')
im.shape
type(im)
get_ipython().run_line_magic('pwd', '')
import pathlib
root = pathlib.Path('.')
get_ipython().run_line_magic('pinfo', 'str.endswith')
for p in root.rglob('*'):
    if p.endswith(('zarr', 'nd2', 'tif', 'tiff')):
        print(p)
        print(p.name)
for p in root.rglob('*'):
    if str(p).endswith(('zarr', 'nd2', 'tif', 'tiff')):
        print(p)
        print(p.name)
        print(str(p))
        
zim = imread('segmentation/invivo_example/ground_truth/medium - control/saline_example_GT_PL.zarr')
import zarr
zim = np.asarray(zarr.open('segmentation/invivo_example/ground_truth/medium - control/saline_example_GT_PL.zarr'))
zim.shape
import tifffile
map_open = {
    'tif': tifffile.imread,
    'zarr': lambda fn: np.asarray(zarr.open(fn)),
    'nd2': imread,
    }
(1,) * 0
images = [p for p in root.rglob('*')
    if str(p).endswith(('zarr', 'nd2', 'tif', 'tiff'))]
p = images[0]
p.parent
new_root = pathlib.Path('/Users/jni/Dropbox/data/finding-and-following/')
p.suffix
set(f.suffix for f in images)
p.name
p.root
p.parts
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
    
get_shape = lambda fn: tz.pipe(fn, open, json.load, tz.curried.get('scale'), tuple)
g
m = glob('**/*.json', root_dir='./metadata', recursive=True)
m
all_scales = set(map(get_scale, m))
get_scale = lambda fn: tz.pipe(fn, open, json.load, tz.curried.get('scale'), tuple)
all_scales = set(map(get_scale, m))
m = glob('**/*.json', root_dir='.', recursive=True)
m
all_scales = set(map(get_scale, m))
all_scales
get_ch = lambda fn: tz.pipe(fn, open, json.load, tz.curried.get('channels'), tuple)
all_chs := set(map(get_ch, m))
all_chs = set(map(get_ch, m)); all_chs
