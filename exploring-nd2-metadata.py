# IPython log file


from pims_nd2 import ND2_Reader as ND2
image = ND2('200519_IVMTR69_Inj4_dmso_exp3.nd2')
image.sizes
print(image.metadata_text)
print(image.metadata)
image.axes
image.calibration
image.calibrationZ
image.colors
image.frame_rate
image.frame_shape
image.pixel_type
image.propagate_attrs
get_ipython().run_line_magic('ls', '')
get_ipython().system('head 200519_IVMTR69_Inj4_dmso_exp3_Position.csv')
track_positions = pd.read_csv('200519_IVMTR69_Inj4_dmso_exp3_Position.csv', header=0)
get_ipython().run_line_magic('debug', '')
track_positions = pd.read_csv('200519_IVMTR69_Inj4_dmso_exp3_Position.csv', header=0, skiprows=2)
track_positions.shape
get_ipython().run_line_magic('pinfo', 'pd.read_csv')
track_positions = pd.read_csv('200519_IVMTR69_Inj4_dmso_exp3_Position.csv', header=0, skiprows=(0, 1))
track_positions.shape
track_positions = pd.read_csv('200519_IVMTR69_Inj4_dmso_exp3_Position.csv', header=2, skiprows=(0, 1))
track_positions.head()
get_ipython().system('head 200519_IVMTR69_Inj4_dmso_exp3_Position.csv')
track_positions = pd.read_csv('200519_IVMTR69_Inj4_dmso_exp3_Position.csv', header=1, skiprows=(0,))
track_positions = pd.read_csv('200519_IVMTR69_Inj4_dmso_exp3_Position.csv', header=0, skiprows=(0,))
track_positions = pd.read_csv('200519_IVMTR69_Inj4_dmso_exp3_Position.csv', header=0, skiprows=(0, 1, 2))
track_positions.head()
track_positions.describe()
track_positions['Position X'].max() - track_positions['Position X'].min()
track_positions['Position Y'].max() - track_positions['Position Y'].min()
track_positions['Position Z'].max() - track_positions['Position Z'].min()
image.shape
image.sizes
track_positions[[f'Position {i}' for i in 'XYZ']].describe()
2182 - 256 * 0.504
2182 + 256 * 0.504
2055 - 256 * 0.504
2055 + 256 * 0.504
from nd2reader import ND2Reader as NND2
nimage = NND2('200519_IVMTR69_Inj4_dmso_exp3.nd2')
nimage.metadata
image.metadata
from nd2reader import raw_metadata
meta = raw_metadata.RawMetadata(nimage.filename)
nimage._get_metadata_property
nimage._default_coords
get_ipython().run_line_magic('pinfo', 'nimage._get')
get_ipython().run_line_magic('pinfo', 'raw_metadata.read_metadata')
from nd2reader import Nd2
nnimage = Nd2('/Users/jni/Dropbox/share-files/200519_IVMTR69_Inj4_dmso_exp3.nd2')
nnimage.height
nnimage.pixel_microns
nnimage.frames
nnimage.z_levels
get_ipython().run_line_magic('pinfo', 'nnimage.get_image')
get_ipython().run_line_magic('pinfo', 'nnimage.reader')
nimage.parser._raw_metadata
nimage.parser._raw_metadata.image_metadata
nimage.parser._raw_metadata.image_calibration
nimage.parser._raw_metadata.image_metadata
nimage.parser._raw_metadata.pfs_offset
nimage.parser._raw_metadata.get_parsed_metadata()
nimage.parser._raw_metadata.x_data
len(nimage.parser._raw_metadata.x_data)
nimage.sizes
33 * 194 * 4
4 * 194
nimage.parser._raw_metadata.y_data[0]
nimage.parser._raw_metadata.z_data[0]
nimage.parser._raw_metadata.z_data
nimage.parser._raw_metadata.pixel_microns
nimage.parser._raw_metadata.z_coordinates
nimage.parser._raw_metadata.z_levels
nimage.parser._raw_metadata.x_data
nimage.parser._raw_metadata.image_text_info
nimage.parser._raw_metadata.experiment
nimage.parser._raw_metadata.channels
nimage.parser._raw_metadata.image_calibration
nimage.parser._raw_metadata.image_events
next(nimage.parser._raw_metadata.image_events)
nimage.parser._raw_metadata.image_metadata_sequence
def getpath(nested_dict, value, prepath=()):
    for k, v in nested_dict.items():
        path = prepath + (k,)
        if v == value: # found value
            return path
        elif hasattr(v, 'items'): # v is a dict
            p = getpath(v, value, path) # recursive call
            if p is not None:
                return p
getpath(_83, 2.0)
def getpath(nested_dict, value, prepath=(), result=[]):
    for k, v in nested_dict.items():
        path = prepath + (k,)
        if v == value: # found value
            result.append(path)
        elif hasattr(v, 'items'): # v is a dict
            getpath(v, value, path, result) # recursive call
            
getpath(_83, 2.0, result=res:=[])
res = []
getpath(_83, 2.0, result=res)
res
res = []
getpath(_83, -32, result=res); print(res)
getpath(_83, -32.0, result=res); print(res)
getpath(_83, 32.0, result=res); print(res)
getpath(_83, 32, result=res); print(res)
def getkey(nested_dict, key, prepath=(), result=[]):
    for k, v in nested_dict.items():
        path = prepath + (k,)
        if key in k: # found value
            result.append(path)
        elif hasattr(v, 'items'): # v is a dict
            getkey(v, key, path, result) # recursive call
            
getkey(_83, 'dZ', result=res)
getkey(_83, b'dZ', result=res)
res
_83[b'SLxPictureMetadata'][b'dZAxisCalibration']
_83[b'SLxPictureMetadata'][b'dZPos']
rawimmeta = nimage.parser._raw_metadata.image_metadata
res2 = []; getkey(rawimmeta, b'dZ', result=res2); res2
def gettup(d, tup):
    if len(tup) == 1:
        return d[tup[0]]
    else:
        return gettup(d[tup[0]], tup[1:])
        
gettup(rawimmeta, res2[-1])
gettup(rawimmeta, res2[-2])
gettup(rawimmeta, res2[0])
gettup(rawimmeta, res2[1])
image.metadata
x = y = 1
x
y
raw_meta_seq = _83
getkey(raw_meta_seq, 'XPos')
getkey(raw_meta_seq, b'XPos')
def getkey(nested_dict, key, prepath=(), result=[]):
    for k, v in nested_dict.items():
        path = prepath + (k,)
        if key in k: # found value
            result.append(path)
        elif hasattr(v, 'items'): # v is a dict
            getkey(v, key, path, result) # recursive call
    return result
            
getkey(raw_meta_seq, b'XPos')
getkey(raw_meta, b'XPos')
raw_meta = rawimmeta
getkey(raw_meta, b'XPos')
getkey(raw_meta, b'YPos')
def getkey(nested_dict, key, prepath=(), result=None):
    if result is None:
        result = []
    for k, v in nested_dict.items():
        path = prepath + (k,)
        if key in k: # found value
            result.append(path)
        elif hasattr(v, 'items'): # v is a dict
            getkey(v, key, path, result) # recursive call
    return result
            
getkey(raw_meta, b'YPos')
getkey(raw_meta, b'XPos')
import ipdb
import pdb
pdb.runcall(getkey, raw_meta, b'XPos')
raw_meta
getkey(raw_meta_seq, b'XPos')
getkey(raw_meta_seq, b'YPos')
getkey(raw_meta_seq, b'ZPos')
getkey(raw_meta_seq, _131[0])
gettup(raw_meta_seq, _131[0])
gettup(raw_meta_seq, _130[0])
image.sizes
track_positions.columns
track_positions[[f'Position {i}' for i in 'XYZ'] + ['Time']].head()
track_positions['Time'].describe()
meta = {'scale': [1, 4, 1, 1]}
{'hello': 1, **meta}
