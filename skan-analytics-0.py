# IPython log file


dat = pd.read_csv('skeletons.csv', header=0)
dat['cell-type'] = [f.split('_')[-2][0] for f in dat['filename']]
dat.head()
selector = ((dat['branch-type'] == 2) &
            (dat['squiggle'] > 0.001) &
            (dat['squiggle'] < 2))
dat[selector].boxplot(column='branch-distance', by='cell-type')
dat['branch distance (nm)'] = dat['branch-distance'] * 1e9
dat['cell type'] = dat['cell-type']
dat[selector].boxplot(column='branch distance (nm)', by='cell type')
dat[selector].groupby('cell type').median()['branch distance (nm)']
dat['filename'].head()
localdir = '/Users/jni/Dropbox/data/malaria/adam-mix4/'
import os
dat['local filename'] = [os.path.join(localdir, os.path.basename(b))
                         for b in dat['filename']]
import imageio
jtj = dat[selector]
jtj_counts = jtj.groupby('local filename').count()
filenames = set(jtj['local filename'])
scales = {}
for f in filenames:
    try:
        scale = float(imageio.imread(f, format='fei').meta['Scan']['PixelHeight'])
    except OSError:
        scale = np.nan
    scales[f] = scale
    
rows = {}
cols = {}
for f in filenames:
    try:
        image = imageio.imread(f, format='fei')
        nrow, ncol = image.shape[:2]
    except OSError:
        nrow, ncol = np.nan, np.nan
    rows[f] = nrow
    cols[f] = ncol
    
s_rows = pd.Series(rows, name='number of rows')
s_cols = pd.Series(cols, name='number of cols')
s_scales = pd.Series(scales, name='scale (m)')
image_info = pd.concat([s_scales, s_rows, s_cols], axis=1)
counts = jtj_counts['branch-distance']
image_info = image_info.join(counts, how='inner')
image_info['scale (nm)'] = image_info['scale (m)'] * 1e9
image_info['filename'] = image_info.index
image_info.index = [os.path.basename(i) for i in image_info.index]
image_info['cell type'] = [s.split('_')[-2][0] for s in image_info.index]
image_info['branches per nm^2'] = (
    image_info['branch-distance'] /
    (image_info['number of rows'] * image_info['number of cols']
     * image_info['scale (nm)'] ** 2)
)
image_info['branches per µm^2'] = image_info['branches per nm^2'] * 1e6
image_info.boxplot(column='branches per µm^2', by='cell type')
