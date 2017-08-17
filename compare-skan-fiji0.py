# IPython log file


from tifffile import TiffFile
from skimage.external.tifffile import TiffFile
f = TiffFile('OP_1_Rendered_Paths.tif')
p = f[0]
type(p)
p.info()
1 / 0.3033534
skel0 = np.array(p)
skel0.shape
skel0 = p.asarray()
skel0.shape
spacing = [0.3033534 * 3, 0.3033534, 0.3033534]
from skimage import morphology
skel1 = morphology.skeletonize_3d(skel0)
np.allclose(skel0, skel1)
skel0.max()
skel1.max()
np.sum(skel0 != skel1)
io.imsave('OP_1_Rendered_Paths_thinned.tif', skel1)
from skimage import io
io.imsave('OP_1_Rendered_Paths_thinned.tif', skel1)
skel1.shape
skel1.dtype
skel1.max()
skel1.min()
np.sum(skel1==255)
np.sum(skel0==255)
np.unique(skel1)
0.3033534 * 3
3033534 / 10**6 * 3
from skan import csr
get_ipython().magic('pinfo csr.summarise')
spacing = 10 * np.array(spacing)
df = csr.summarise(skel1.astype(bool), spacing=spacing)
df.shape
df.head()
df2 = pd.read_excel('OP_1-Branch-information.xls')
df2 = pd.read_excel('OP_1-Branch-information.xlsx')
df2.shape
df2.head()
df.head()
plt.hist(df['branch-distance'], bins='auto')
plt.hist(df2['Branch length'], bins=_[1], alpha=0.3)
df.shape
df2.shape
np.sum(_42[0])
np.sum(_43[0])
np.sum(np.isnan(df2['Branch length']))
np.min(df2['Branch length'])
np.min(df['Branch length'])
np.min(df['branch-distance'])
dfs = df.sort_values(by='branch-distance', ascending=False)
df2s = df2.sort_values(by='Branch length', ascending=False)
dfs2.head(10)
dfs.head(10)
df2s.head(10)
plt.plot(df2s['Branch length'][:-2], dfs['branch-distance'])
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['coord-0-1'], df['coord-0-2'], df['coord-0-0'])
ax.scatter(df['coord-1-1'], df['coord-1-2'], df['coord-1-0'])
ax.clear()
ax.scatter(df['coord-1-1'], df['coord-1-2'], df['coord-1-0'], c='C0')
ax.scatter(df['coord-0-1'], df['coord-0-2'], df['coord-0-0'], c='C0')
ax.scatter(df2['V1 x'], df2['V1 y'], df2['V1 z'], c='C1')
_.remove()
ax.scatter(df2['V1 y'], df2['V1 x'], df2['V1 z'], c='C1')
ax.scatter(df2['V2 y'], df2['V2 x'], df2['V2 z'], c='C1')
ax.clear()
ax.scatter(df['coord-1-1'], df['coord-1-2'], df['coord-1-0'], c='C0',)
ax.clear()
ax.scatter(df['coord-1-1'], df['coord-1-2'], df['coord-1-0'], c='C0',
           depthshade=False, alpha=0.5)
           
ax.scatter(df['coord-0-1'], df['coord-0-2'], df['coord-0-0'], c='C0',
           depthshade=False, alpha=0.5)
           
ax.scatter(df2['V2 y'], df2['V2 x'], df2['V2 z'], c='C1',
           depthshade=False, alpha=0.5)
           
ax.scatter(df2['V1 y'], df2['V1 x'], df2['V1 z'], c='C1',
           depthshade=False, alpha=0.5)
           
from scipy.spatial import distance_matrix
coords0 = df[['coord-0-0', 'coord-0-1', 'coord-0-2']].values
coords1 = df[['coord-1-0', 'coord-1-1', 'coord-1-2']].values
dm = distance_matrix(coords0, coords1)
np.where(np.min(dm, axis=0))
np.where(np.min(dm, axis=0) > 1e-6)
np.where(np.min(dm, axis=0) > 1e-2)
len(np.where(np.min(dm, axis=0) > 1e-2)[0])
np.where(np.min(dm, axis=1) > 1e-2)
all_points_skan = np.concatenate([coords0, coords1[np.where(np.min(dm, axis=0) > 1e-6)[0]]], axis=0)
all_points_skan.shape
coords0fj = df2[['V1 z', 'V1 y', 'V1 x']]
coords0fj = df2[['V1 z', 'V1 y', 'V1 x']].values
coords1fj = df2[['V2 z', 'V2 y', 'V2 x']].values
dmfj = distance_matrix(coords0fj, coords1fj)
all_points_fiji = np.concatenate([coords0fj, coords1fj[np.where(np.min(dmfj, axis=0) > 1e-6)[0]]], axis=0)
all_points_fiji.shape
dmx = distance_matrix(all_points_skan, all_points_fiji)
assignments = np.argmin(dmx, axis=1)
np.max(dmx[np.arange(dmx.shape[0], assignments)])
np.max(dmx[np.arange(dmx.shape[0]), assignments])
plt.hist(dmx[np.arange(dmx.shape[0]), assignments], bins='auto')
plt.hist(dmx[np.arange(dmx.shape[0]), assignments], bins='auto')
dmx.shape
im0 = np.array([[1, 0, 0, 0, 1],
                [0, 1, 0, 1, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 1, 0, 0],
                [1, 1, 0, 1, 0]], dtype=bool)
                
io.imsave('test-image0.png', im0)
im0 = np.vstack([im0[:3], im0[3:4], im0[3:]])
im0
io.imsave('test-image0.png', im0)
csr.summarise(im0)
get_ipython().magic('pwd ')
plt.set_xlabel('Distance from skan skeleton point\nto nearest Fiji skeleton point')
plt.xlabel('Distance from skan skeleton point\nto nearest Fiji skeleton point')
plt.xlabel('Distance from skan skeleton point\nto nearest Fiji skeleton point (')
plt.xlabel('Distance from skan skeleton point\nto nearest Fiji skeleton point (µm)')
plt.ylabel('count')
plt.tight_layout()
plt.savefig('nearestpoint_OP1.png')
plt.hist(df['branch-distance'], bins='auto');
plt.hist(df2['Branch length'], bins='auto', label='Fiji');
plt.hist(df['branch-distance'], bins=_[1], label='skan', alpha=0.3);
res = plt.hist(df2['Branch length'], bins='auto', label='Fiji')
res
plt.hist(df['branch-distance'], bins=res[1], label='skan', alpha=0.3);
df['branch-distance'].max()
get_ipython().magic('pinfo np.histogram')
bins = np.histogram(np.concatenate((df['branch-distance'],
                                    df2['Branch length'])),
                    bins='auto')[1]
                    
bins
