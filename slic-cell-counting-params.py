# IPython log file

import numpy as np
array = np.array
from skimage import data, color
from skimage import filter as imfilter
import sys
sys.path.append('/Users/nuneziglesiasj/projects/gala')
from gala import morpho
from gala import viz
import pdb
from skimage.segmentation import slic
from gala import imio
dorsal = imio.read_image_stack('/Users/nuneziglesiasj/Data/armi-data/cyril-sample-images/dorsal1-d5/png/*.png')
dorsal.shape
dorsal.max()
dorsal = dorsal.astype(float)/255
#sdors = slic(dorsal, 1000, ratio=5, sigma=array([0.2, 1, 1, 0]), multichannel=True, convert2lab=False)
#sdors = slic(dorsal, 500, ratio=20, sigma=array([0.2, 1, 1, 0]), multichannel=True, convert2lab=False)
#sdors = slic(dorsal, 500, ratio=40, sigma=array([0.2, 1, 1, 0]), multichannel=True, convert2lab=False)
#sdors = slic(dorsal, 500, ratio=1, sigma=array([0.2, 1, 1, 0]), multichannel=True, convert2lab=False)
#sdors = slic(dorsal, 500, ratio=3.5, sigma=array([0.2, 1, 1, 0]), multichannel=True, convert2lab=False)
sdors = slic(dorsal, 1000, ratio=3.5, sigma=array([0.2, 1, 1, 0]), multichannel=True, convert2lab=False)
sdorsim = viz.draw_seg(sdors, dorsal)
