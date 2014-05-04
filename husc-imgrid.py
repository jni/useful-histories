# IPython log file


from skimage import io
import os
fns = os.listdir
fns = os.listdir('.')
get_ipython().set_next_input(u'fns = filter');get_ipython().magic(u'pinfo filter')
fns = filter(lambda x: x.endswith('illum-95-51.tif'), fns)
len(fns)
fns = sorted(fns)
images = []
for r, g, b in [fns[i:i+3] for i in range(48)]:
    images.append(np.dstack([io.imread(j) for j in [r, g, b]]))
    
imshow(images[0])
images = []
for g, b, r in [fns[i:i+3] for i in range(48)]:
    images.append(np.dstack([io.imread(j) for j in [r, g, b]]))
    
len(images)
imshow(images[0])
sample_names = list(it.product('CDE', ['%02i'%j for j in range(3, 23)]))
import itertools as it
sample_names = list(it.product('CDE', ['%02i'%j for j in range(3, 23)]))
sample_names = [i+j for i, j in sample_names]
sample_names = sample_names[1:-11]
def imgrid(names, grid_shape):
    figure()
    idxs = [sample_names.find(name) for name in names]
    sh = grid_shape
    for i, idx in enumerate(idxs):
        subplot(sh + (i+1,))
        imshow(images[idx], interpolation='nearest')
        
imgrid(['D14', 'D16', 'D17', 'D15', 'D18'], (2, 3))
def imgrid(names, grid_shape):
    figure()
    idxs = [sample_names.index(name) for name in names]
    sh = grid_shape
    for i, idx in enumerate(idxs):
        subplot(sh + (i+1,))
        imshow(images[idx], interpolation='nearest')
        
imgrid(['D14', 'D16', 'D17', 'D15', 'D18'], (2, 3))
get_ipython().magic(u'pinfo subplot')
def imgrid(names, grid_shape):
    figure()
    idxs = [sample_names.index(name) for name in names]
    sh = grid_shape
    for i, idx in enumerate(idxs):
        subplot(*(sh + (i+1,)))
        imshow(images[idx], interpolation='nearest')
        
imgrid(['D14', 'D16', 'D17', 'D15', 'D18'], (2, 3))
fns[:6]
imshow(images[1])
images = []
for g, b, r in [fns[3*i:3*i+3] for i in range(48)]:
    images.append(np.dstack([io.imread(j) for j in [r, g, b]]))
    
len(images)
imgrid(['D14', 'D16', 'D17', 'D15', 'D18'], (2, 3))
images = []
for r, b, g in [fns[3*i:3*i+3] for i in range(48)]:
    images.append(np.dstack([io.imread(j) for j in [r, g, b]]))
    
imgrid(['D14', 'D16', 'D17', 'D15', 'D18'], (2, 3))
for im, sn in zip(images, sample_names):
    io.imsave(sn+'.illum-95-51.rbg.tif', im)
    
imgrid(['C16', 'C17', 'D13'], (1, 3))
imgrid(['C09', 'C18', 'C22'], (1, 3))
imgrid(['C11', 'C12', 'C21', 'E07'], (2, 2))
imgrid(['C04', 'C08'], (1, 2))
imgrid(['D06', 'D22'], (1, 2))
imgrid(['D08', 'D20'], (1, 2))
imgrid(['E08', 'C14', 'E03'], (1, 3))
imgrid(['E08', 'C14', 'E03', 'E09', 'C05'], (2, 3))
imgrid(['C16', 'C17', 'D13', 'C09', 'C18', 'C22'], (2, 3))
imgrid(['C11', 'C12', 'C21', 'E07'], (2, 2))
