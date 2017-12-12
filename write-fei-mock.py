# IPython log file


glob
from glob import glob
filenames0 = glob('/Users/jni/Dropbox/data1/malaria/adam-retic/*.tif')
filenames1 = glob('/Users/jni/Dropbox/data1/malaria/adam-gametocytes-gh9-catherine/*.tif')
len(filenames0)
len(filenames1)
filenames2 = [f for f in filenames1 if not f.endswith('01.tif')]
len(filenames2)
filenames3 = [f for f in filenames0 if not f.endswith('01.tif')]
len(filenames3)
images_iter = (iio.imread(filename, format='fei')
               for filename in filenames2 + filenames3)
               
for fn, im in zip(filenames2 + filenames3, images_iter):
    io.imsave(fn[:-4] + '.png', im)
    
def get_scale(fn):
    im = iio.imread(fn)
    scale = float(im.meta['Scan']['PixelHeight'])
    return scale
scales = [get_scale(fn) for fn in filenames2]
def get_scale(fn):
    im = iio.imread(fn, format='fei')
    scale = float(im.meta['Scan']['PixelHeight'])
    return scale
scales = [get_scale(fn) for fn in filenames2]
scales
len(scales)
len(set(scales))
im.shape
get_ipython().magic('pinfo iio.imsave')
iio.help()
iio.help('PNG')
iio.help('TIFF')
iio.help()
help('FITS')
iio.help('FITS')
len(set(get_scale(fn) for fn in filenames3))
len([get_scale(fn) for fn in filenames3])
[get_scale(fn) for fn in filenames3]
from astropy import io
get_ipython().magic('pinfo io.imsave')
dir(io)
from skimage import io
iio.help('FITS-PIL')
iio.help('FITS')
iio.help()
fn
im.name
im.filename
im.file
im = iio.imread(fn, format='fei')
iio.imsave(os.path.expanduser('~/Desktop/') +fn[:-4] + '.tiff', im)
iio.imsave(os.path.expanduser('~/Desktop/') + os.path.basename(fn)[:-4] + '.tiff', im)
lastfn = os.path.expanduser('~/Desktop/') + os.path.basename(fn)[:-4]
 + '.tiff'
lastfn = os.path.expanduser('~/Desktop/') + os.path.basename(fn)[:-4] + '.tiff'
im2 = iio.imread(lastfn)
im2.meta
iio.imsave(lastfn, im, meta={'resolution': str(get_scale(fn)}))
iio.imsave(lastfn, im, meta={'resolution': str(get_scale(fn))})
scale = get_scale(fn)
iio.help('TIFF')
im.meta['resolution'] = scale
iio.imsave(lastfn, im)
im.meta['resolution'] = (scale, scale)
iio.imsave(lastfn, im)
imreload = iio.imread(lastfn)
imreload.meta['resolution']
imreload.meta
iio.help('TIFF')
imreload.meta['resolution_unit']
im.meta['resolution_unit'] = (scale, scale)
iio.imsave(lastfn, im)
imreload.meta['resolution_unit']
imreload = iio.imread(lastfn)
imreload.meta
str(scale).encode('ascii')
scale_str = b'[Scan]\nPixelHeight=' + str(scale).encode('ascii')
scale_str
get_ipython().magic('pinfo open')
with open(lastfn, 'a') as fout:
    fout.write(scale_str)
with open(lastfn, 'ab') as fout:
    fout.write(scale_str)
imreload2 = iio.imread(lastfn, format='fei')
iio.imsave(lastfn, im)
scale_str = b'[root]\nfoo=bar\n[Scan]\nPixelHeight=' + str(scale).encode('ascii')
with open(lastfn, 'ab') as fout:
    fout.write(scale_str)
imreload2 = iio.imread(lastfn, format='fei')
iio.imsave(lastfn, im)
scale_str = b'\n[root]\nfoo=bar\n[Scan]\nPixelHeight=' + str(scale).encode('ascii')
with open(lastfn, 'ab') as fout:
    fout.write(scale_str)
imreload2 = iio.imread(lastfn, format='fei')
scale_str = b'\r\nDate=13/10/2017\r\n[Scan]\r\nPixelHeight=' + str(scale).encode('ascii') + b'\r\n'
iio.imsave(lastfn, im)
with open(lastfn, 'ab') as fout:
    fout.write(scale_str)
imreload2 = iio.imread(lastfn, format='fei')
imreload2.meta['Scan']['PixelHeight']
def write_fei_mock(image, scale, fn):
    image2 = np.pad(image, ((0, 70), (0, 0)), cval=0)
    scale_hdr = b'\r\nDate=13/10/2017\r\n[Scan]\r\nPixelHeight='
    scale_str = scale_hdr + str(scale).encode('ascii') + b'\r\n'
    iio.imsave(fn, image2)
    with open(fn, 'ab') as fout:
        fout.write(scale_str)
fn
improb = iio.imread(fn[:-4] + '_Probabilities.png')
plt.imshow(improb)
plt.imshow(improb[..., 0], cmap='magma')
plt.figure(); plt.imshow(im, cmap='gray')
