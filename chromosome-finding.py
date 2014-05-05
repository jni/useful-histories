# IPython log file

import numpy as np
from skimage import io
import os
get_ipython().magic(u'cd /Users/nuneziglesiasj/Dropbox/RNAPII\\ Quant\\ Juan')
ims = [io.imread(fn) for fn in filter(lambda x: x.endswith('.tif'), sorted(os.listdir('.')))]
map(np.shape, ims)
imshow(ims[0])
hr, hg, hb = [np.histogram(ims[0][..., i], bins=255) for i in range(3)]
type(hr)
map(type, hr)
histogram(hr)
for h in [hr, hg, hb]:
    plot(h[1], h[0])
    
get_ipython().magic(u'pinfo plot')
map(len, hr)
for h in [hr, hg, hb]:
    plot(h[1][:-1], h[0])
    
im = ims[0]
[(im[..., i].min(), im[..., i].max()) for i in range(3)]
from skimage import filter as skfilter
t = skfilter.threshold_otsu(im)
t
ts = [skfilter.threshold_otsu(im[..., i]) for i in range(3)]
ts
r, g, b = [im[..., i] for i in range(3)]
figure(); imshow(r > 17)
figure(); imshow(g > 28)
figure(); imshow(b > 42)
tsa = [skfilter.threshold_adaptive(im[..., i], 51) for i in range(3)]
tsa
figure(); imshow(tsa[0]); figure(); imshow(tsa[1]); figure(); imshow(tsa[2])
chromart = tsa[2].astype(uint8) * 255
get_ipython().magic(u'pinfo io.imsave')
io.imsave('chromosome art.tif', chromart)
chromart = dstack(chromart, zeros_like(chromart), 255-chromart)
chromart = dstack((chromart, zeros_like(chromart), 255-chromart))
io.imsave('chromosome art 2.tif', chromart)
adr, adg, adb = tsa
from scipy import ndimage as nd
get_ipython().set_next_input(u'chrs = nd.label');get_ipython().magic(u'pinfo nd.label')
str2 = nd.generate_binary_structure(2, 2)
chrs = nd.label(adb, str2)[0]
figure(); imshow(chrs)
sizes = bincount(chrs)
sizes = bincount(chrs.ravel())
figure(); hist(sizes, 100)
get_ipython().magic(u'pinfo hist')
figure(); _ = hist(sizes, 100, range=(43000, sizes.max()))
from skimage import morphology as skmorph
get_ipython().set_next_input(u'chrs_a = skmorph.remove_small_objects');get_ipython().magic(u'pinfo skmorph.remove_small_objects')
chrs_a = skmorph.remove_small_objects(chrs, 8000)
figure(); imshow(chrs_a)
chrs_a = skmorph.remove_small_objects(chrs, 9000)
figure(); imshow(chrs_a)
chrs_a = skmorph.remove_small_objects(chrs, 20000)
figure(); imshow(chrs_a)
chrs_a = skmorph.remove_small_objects(chrs, 15000)
figure(); imshow(chrs_a)
chrs_a = skmorph.remove_small_objects(chrs, 12500)
figure(); imshow(chrs_a)
chrs_a = skmorph.remove_small_objects(chrs, 11000)
figure(); imshow(chrs_a)
chrs_a = skmorph.remove_small_objects(chrs, 10000)
figure(); imshow(chrs_a)
chrs_a = skmorph.remove_small_objects(chrs, 10500)
figure(); imshow(chrs_a)
chrs_a = skmorph.remove_small_objects(chrs, 11000)
chrs_b = skmorph.remove_small_objects(chrs, 1000)
chrs_c = chrs_b - chrs_a
figure(); imshow(chrs_c)
chrs_b = skmorph.remove_small_objects(chrs, 2000)
figure(); imshow(chrs_b - chrs_a)
