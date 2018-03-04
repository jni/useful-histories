# IPython log file

import os
os.chdir('/Users/jni/Dropbox/data1/malaria/adam-oli-schizont-30sec')

import imageio as iio
im = iio.imread('Shchizont4_UninfRBC10_02.tif', format='fei')
scale = im.meta['Scan']['PixelHeight'] * 1e9  # convert m to nm
sigma = 5/scale  # nm / (nm/pixel) ==> pixel

import matplotlib.pyplot as plt
plt.imshow(im, cmap='gray')

from skan import pre
from skimage import morphology
binary = pre.threshold(im, sigma=sigma, radius=round(10*sigma))
skeleton_image = morphology.skeletonize(binary)
plt.imshow(skeleton_image)

shape = feature.shape_index(im, sigma=5)
plt.imshow(shape, cmap='RdBu')

shape_skeleton = skeleton_image * shape

from skan import summarise

data = summarise(shape_skeleton)
data.head()

from skan import draw
draw.overlay_skeleton_2d(im, shape_skeleton, dilate=1)

def filtered(values):
    return np.digitize(values, [0.125, 0.625])

data['filtered'] = filtered(data['mean pixel value'])
draw.overlay_euclidean_skeleton_2d(im, data,
                                   skeleton_color_source='filtered')

from skan import Skeleton
skeleton = Skeleton(shape_skeleton, source_image=im)
# second time is much faster thanks to Numba JIT
skeleton = Skeleton(shape_skeleton, source_image=im)

def filtered2(skeleton):
    values = skeleton.path_means()
    return filtered(values)

ax, cvals = draw.overlay_skeleton_2d_class(skeleton,
                                           skeleton_color_source=filtered2)

