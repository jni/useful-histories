# IPython log file


import toolz as tz
import numpy as np
from skimage import io
import os
filenames = sorted(os.listdir())
from toolz import curried as c
os.makedirs('8bit')
# find the maximum value over all images
tz.pipe(filenames, c.map(io.imread), c.map(np.max), max)
import sys
sys.path.append('/Users/nuneziglesiasj/projects/microscopium')
from microscopium import preprocess as pre
# get an image of representative intensity over all input images
sampled = tz.pipe(filenames, c.map(io.imread), pre._reservoir_sampled_image)
from skimage import exposure
hist = exposure.histogram(sampled)
from matplotlib import pyplot as plt
plt.plot(hist[1], hist[0])
in_range = tuple(np.percentile(sampled.ravel(), [1, 99]))
for filename in filenames:
    image = io.imread(filename)
    out = exposure.rescale_intensity(image, in_range=in_range,
                                     out_range=(0, 255))
    out = out.astype(np.uint8)
    io.imsave('8bit/' + filename[:-3] + 'tif', out,
              plugin='tifffile', compress=1)
    
filenames8 = sorted(os.listdir('8bit/'))[1:]  # ignore .DS_Store
filenames8 = [os.path.join('8bit', fn) for fn in filenames8]
sampled8 = tz.pipe(filenames8, c.map(io.imread), pre._reservoir_sampled_image)
freq, bin = exposure.histogram(sampled8)
plt.figure()
plt.plot(bin, freq)
