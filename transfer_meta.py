from pathlib import Path
import numpy as np
import json
import os
import zarr
import sys
from copy import deepcopy
from ome_zarr.io import parse_url
from ome_zarr.writer import write_image
from tqdm import tqdm


def read_json(fn):
    return json.load(open(fn))


def update_nested(input_dict, tuple_updates):
    """Update the input dictionary at the given nested keys.

    Examples
    --------
    >>> d = {'hello': 'world', 'foo': {'bar': 5}}
    >>> d2 = update_nested(d, {('foo', 'bar'): 7})
    >>> print(d2)
    {'hello': 'world', 'foo': {'bar': 7}}
    >>> d3 = update_nested(d, {'foo.bar': 7})
    >>> print(d3)
    {'hello': 'world', 'foo': {'bar': 7}}
    """
    out = deepcopy(input_dict)
    for multi_key, multi_value in tuple_updates.items():
        if not isinstance(multi_key, tuple):
            multi_key = multi_key.split('.')
        d = out
        for key in multi_key[:-1]:
            d = d.setdefault(key, {})
        d[multi_key[-1]] = multi_value
    return out


metadata_root = Path('/Users/jni/data/FindingAndFollowing/metadata/')
data_root = Path('/Users/jni/Dropbox/data/finding-and-following/')
new_data_root = Path('/Users/jni/Dropbox/data/finding-and-following-ome/')
os.makedirs(new_data_root, exist_ok=True)

colors = {
    'GaAsP Alexa 488': '00ff00',  # green
    'GaAsP Alexa 568': 'ff0000',  # red
    'Alxa 647': 'ff00ff',  # magenta
    'TD': 'ffffff',  # grayscale
}


def print_diagnostics(**kwargs):
    for k, v in kwargs.items():
        print(f'{k}={v}')


scale = (3.125, 1, 2.0, -0.504248154773493, -0.504248154773493)

base_axes = [{'name': 't', 'type': 'time', 'unit': 'second'},
        {'name': 'c', 'type': 'channel'},
        {'name': 'z', 'type': 'space', 'unit': 'micrometer'},
        {'name': 'y', 'type': 'space', 'unit': 'micrometer'},
        {'name': 'x', 'type': 'space', 'unit': 'micrometer'},]

base_coord_tfs = [[{'scale': scale[2:], 'type': 'scale'}]]
multichannel_coord_tfs = [[{'scale': scale[1:], 'type': 'scale'}]]
time_coord_tfs = [[{'scale': (scale[0],) + scale[2:], 'type': 'scale'}]]
time_multichannel_coord_tfs = [[{'scale': scale, 'type': 'scale'}]]

visible = {k: (v != 'TD') for k, v in colors.items()}

metadata_files = list(metadata_root.rglob('*.json'))
metadata_parents = {str(f.parent.relative_to(metadata_root)): metadata_root / f
                    for f in metadata_files}

def get_meta(path):
    for d in metadata_parents:
        if d in str(path):
            return read_json(metadata_parents[d])

def is_timeseries(arr):
    return arr.ndim > 3 and arr.shape[0] > 10

data_files = list(data_root.rglob('*.zarr'))

for image_fn in tqdm(data_files):
    parent = str(image_fn.parent.relative_to(data_root))
    new_image_fn = (
            new_data_root / parent / image_fn.stem
            ).with_suffix('.ome.zarr')
    store = parse_url(new_image_fn, mode='w').store
    root = zarr.group(store=store)
    array_data = zarr.open(data_root / image_fn, mode='r')
    if np.issubdtype(array_data.dtype, np.floating):
        array_data_old = array_data
        array_data = np.asarray(array_data, dtype=np.uint16)

    axes = deepcopy(base_axes)
    coord_tfs = time_multichannel_coord_tfs
    multichannel = True
    if not is_timeseries(array_data):
        axes = axes[1:]
        coord_tfs = multichannel_coord_tfs
        if not array_data.ndim > 3:  # not multichannel
            multichannel = False
            axes = axes[1:]
            coord_tfs = base_coord_tfs
    else:  # time series
        if array_data.ndim == 4:  # not multichannel
            multichannel = False
            axes = [axes[0]] + axes[2:]
            coord_tfs = time_coord_tfs

    write_image(
            array_data, group=root, scaler=None, axes=axes,
            coordinate_transformations=coord_tfs,
            storage_options={
                'chunks': (1,) * (array_data.ndim - 3) + array_data.shape[-3:],
            },
            )

    is_labels = array_data.dtype.itemsize > 2
    is_labels2 = get_meta(new_image_fn) is None
    if is_labels != is_labels2:
        print(f'{array_data.dtype.itemsize=} for {image_fn=}')

    print_diagnostics(
            image_fn=image_fn,
            new_image_fn=new_image_fn,
            array_data_shape=array_data.shape,
            array_data_dtype=array_data.dtype,
            multichannel=multichannel,
            metadata=get_meta(new_image_fn),
            )

    if multichannel:
        channels = get_meta(new_image_fn)['channels']
        chdata = []
        for ch in channels:
            for prefix, color in colors.items():
                if ch.startswith(prefix):
                    chdata.append({
                        'color': color,
                        'window': {'start': 0, 'end': 4095},
                        'label': ch,
                        'active': ch != 'TD',
                    })
        root.attrs['omero'] = {'channels': chdata}
    elif is_labels:
        root.attrs['image-label'] = {}
    else:  # single channel
        root.attrs['omero'] = {
            'channels': [{'color': '00ff00',
                          'window': {'start': 0, 'end': 4095},
                          'label': 'all platelets',
                          'active': True,}]
        }
