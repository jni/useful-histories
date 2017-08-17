# IPython log file


from skimage.external.tifffile import TiffFile
f = TiffFile('OP_1_Rendered_Paths.tif')
p = f[0]
skel0 = p.asarray()
spacing = [0.3033534 * 3, 0.3033534, 0.3033534]
from skimage import morphology
skel1 = morphology.skeletonize_3d(skel0)
np.allclose(skel0, skel1)
np.sum(skel0 != skel1)
from skimage import io
# io.imsave('OP_1_Rendered_Paths_thinned.tif', skel1)
skel1 = io.imread('OP_1_Rendered_Paths_thinned.tif')
from skan import csr
spacing = 10 * np.array(spacing)
df = csr.summarise(skel1.astype(bool), spacing=spacing)
df2 = pd.read_excel('OP_1-Branch-information.xlsx')
dfs = df.sort_values(by='branch-distance', ascending=False)
df2s = df2.sort_values(by='Branch length', ascending=False)
from scipy.spatial import distance_matrix
coords0 = df[['coord-0-0', 'coord-0-1', 'coord-0-2']].values
coords1 = df[['coord-1-0', 'coord-1-1', 'coord-1-2']].values
dm = distance_matrix(coords0, coords1)
all_points_skan = np.concatenate([coords0, coords1[np.where(np.min(dm, axis=0) > 1e-6)[0]]], axis=0)
coords0fj = df2[['V1 z', 'V1 y', 'V1 x']].values
coords1fj = df2[['V2 z', 'V2 y', 'V2 x']].values
dmfj = distance_matrix(coords0fj, coords1fj)
all_points_fiji = np.concatenate([coords0fj, coords1fj[np.where(np.min(dmfj, axis=0) > 1e-6)[0]]], axis=0)
dmx = distance_matrix(all_points_skan, all_points_fiji)
assignments = np.argmin(dmx, axis=1)
plt.hist(dmx[np.arange(dmx.shape[0]), assignments], bins='auto')
plt.xlabel('Distance from skan skeleton point\nto nearest Fiji skeleton point (µm)')
plt.ylabel('count')
plt.tight_layout()
#plt.savefig('nearestpoint_OP1.png')
res = plt.hist(df2['Branch length'], bins='auto', label='Fiji')
res
plt.hist(df['branch-distance'], bins=res[1], label='skan', alpha=0.3);
