# IPython log file

from matplotlib import pyplot as plt, cm
imshow = plt.imshow
clf = plt.clf
figure = plt.figure
colorbar = plt.colorbar
hist = plt.hist
import numpy as np
from IPython import get_ipython
import mahotas as mh
import glob
import os
fns = os.listdir('.')
import functools as ft
fnw = ft.partial(glob.fnmatch.fnmatch, pat='*s1*crop*.tif')
fns_nw = filter(fnw, fns)
len(fns_nw)
len(fns_nw) / 3
def intensity(im): return im.sum(axis=-1)
def whiteness(im): return 1 / (np.var(im, axis=-1) + 1)
def artifact(im): return whiteness(im) * intensity(im)
ims_nw = map(mh.imread, fns_nw)
rgbs_nw = [np.dstack(ims_nw[3*i:3*i+3]) for i in range(48)]
imshow(rgbs_nw[0])
imshow(rgbs_nw[1])
imshow(rgbs_nw[5])
rgbs_nw[0].dtype
ims_nw[0].dtype
ims_nw[0].min()
ims_nw[0].max()
ims_nw[1].max()
ims_nw[1].min()
ims_nw[1].dtype
ims_nw[2].dtype
ims_nw[2].min()
ims_nw[2].max()
def cshow(im):
    # assume image data is in the final two dimensions
    if im.ndim > 2:
        mid = im.shape[0] // 2
        cshow(im[mid])
    else:
        plt.imshow(im, cmap=cm.cubehelix, interpolation='nearest')
cshow(ims_nw[0])
cshow(ims_nw[1])
cshow(ims_nw[2])
imshow(rgbs_nw[0])
ims_nw = map(lambda x: (x.astype(float) / x.max() * 255).astype(np.uint8), ims_nw)
ims_nw = map(mh.imread, fns_nw)
rbs_nw = map(lambda x: (x.astype(float) / x.max() * 255).astype(np.uint8), rgbs_nw)
imshow(rgbs_nw[0])
rgbs_nw[0].dtype
imshow(rbs_nw[0])
rbs_nw = map(lambda x: (x.astype(float) / x.max(axis=0).max(axis=0)[None, None, :] * 255).astype(np.uint8), rgbs_nw)
imshow(rbs_nw[0])
cshow(ims_nw[0])
cshow(ims_nw[1])
cshow(ims_nw[2])
rbs_nw = map(lambda x: (x.astype(float) / x.max(axis=0).max(axis=0)[None, None, :] * 255).astype(np.uint8), rgbs_nw)
clf()
imshow(rbs_nw[4])
imshow(rbs_nw[5])
arts_nw = map(artifact, rbs_nw)
cshow(arts_nw[0])
cshow(arts_nw[1])
cshow(arts_nw[2])
cshow(arts_nw[3])
cshow(arts_nw[4])
cshow(arts_nw[5])
max_arts = np.array(map(np.max, arts_nw)).reshape((6, 8))
cshow(max_arts)
figure()
cshow(arts_nw[24])
cshow(arts_nw[25])
cshow(arts_nw[26])
cshow(arts_nw[27])
arts_nw = map(artifact, rbs_nw)
max_arts = np.array(map(np.max, arts_nw)).reshape((6, 8))
cshow(max_arts)
figure()
figure(1)
colorbar()
figure(2)
cshow(arts_nw[5])
cshow(arts_nw[37])
fse = ft.partial(glob.fnmatch.fnmatch, pat='*s4*crop*.tif')
fns_se = filter(fse, fns)
ims_se = map(mh.imread, fns_se)
rgbs_se = [np.dstack([ims_se[j] for j in [3*i+2, 3*i, 3*i+1]]) for i in range(48)]
rbs_se = map(lambda x: (x.astype(float) / x.max(axis=0).max(axis=0)[None, None, :] * 255).astype(np.uint8), rgbs_nw)
arts_se = map(artifact, rbs_se)
max_arts_se = np.array(map(np.max, arts_se)).reshape((6, 8))
figure(1); cshow(max_arts_se)
clf()
cshow(max_arts_se)
rbs_se = map(lambda x: (x.astype(float) / x.max(axis=0).max(axis=0)[None, None, :] * 255).astype(np.uint8), rgbs_se)
arts_se = map(artifact, rbs_se)
max_arts_se = np.array(map(np.max, arts_se)).reshape((6, 8))
cshow(max_arts_se)
figure(); cshow(arts_se[1])
figure(); imshow(rbs_se[1])
figure(); cshow(arts_se[1])
colorbar()
from husc.preprocess import stretchlim
figure(); cshow(stretchlim(arts_se[1]))
def artifact2(im): return np.prod(im, axis=-1)
arts_se2 = map(artifact2, rbs_se)
figure(); cshow(arts_se[1])
figure(); cshow(stretchlim(arts_se[1]))
figure(); cshow(arts_se2[1])
colorbar()
figure(); cshow(stretchlim(arts_se2[1]))
max_arts_se2 = np.array(map(np.max, arts_se2)).reshape((6, 8))
figure(); cshow(max_arts_se2)
colorbar()
figure(); hist(max_arts_se2.ravel())

