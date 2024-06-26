# IPython log file


get_ipython().magic('pwd')
current_directory = '/Users/jni/projects/skan-scripts'
skel1 = io.imread('OP_1_Rendered_Paths_thinned.tif')
from skan import csr
spacing = [3.033534 * 3, 3.033534, 3.033534]
spacing = np.asarray(spacing)
df = csr.summarise(skel1.astype(bool), spacing=spacing)
df2 = pd.read_excel('OP_1-Branch-information.xlsx')
dfs = df.sort_values(by='branch-distance', ascending=False)
df2s = df2.sort_values(by='Branch length', ascending=False)
dfs.shape
df2s.shape
bins = np.histogram(np.concatenate((df['branch-distance'],
                                    df2['Branch length'])),
                    bins=35)[1]
                    
fig, ax = plt.subplots()
ax.hist(df['branch-distance'], bins=bins, label='skan');
ax.hist(df2['Branch length'], bins=bins, label='Fiji', alpha=0.3)
ax.legend();
bins = np.histogram(np.concatenate((df['branch-distance'],
                                    df2['Branch length'])),
                    bins='auto')[1]
                    
fig, ax = plt.subplots()
ax.hist(df['branch-distance'], bins=bins, label='skan');
ax.hist(df2['Branch length'], bins=bins, label='Fiji', alpha=0.3);
get_ipython().magic('pinfo np.histogram')
ax.legend();
ax.set_xlabel('branch length (µm)')
ax.set_ylabel('count')
fig.savefig('OP1-branch-length-histogram-new.png')
get_ipython().magic('cpaste ')
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
from scipy.spatial import distance_matrix
get_ipython().magic('cpaste ')
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
fig, ax = plt.subplots()
ax.hist(dmx[np.arange(dmx.shape[0]), assignments], bins='auto');
dmx.shape
assigments.sape
assignments.shape
dmx[np.arange(dmx.shape[0]), assignments].shape
ax.hist(dmx[np.arange(dmx.shape[0]), assignments], bins='auto');
values = dmx[np.arange(dmx.shape[0]), assignments]
bins = np.histogram(values, bins='auto')[1]
ax.hist(values, bins=bins);
fig, ax = plt.subplots()
ax.hist(values, bins=bins);
counts, bins = np.histogram(values, bins='auto')
counts.shape
bins.shape
counts, bins = np.histogram(values, bins=100)
fig, ax = plt.subplots()
ax.plot(bins[:-1]/2 + bins[1:]/2, counts)
ax.clear()
ax.hist(values, bins=bins);
np.sqrt(9**2 + 3**2 + 3**2)
ax.set_xlabel('distance from skan point to nearest Fiji point (µm)')
ax.set_ylabel('count')
fig.savefig('OP1-point-distance-histogram-new.png')
np.argmax(np.argmin(dmx, axis=1))
np.argmin(dmx[79])
all_points_skan[79]
all_points_fiji[99]
np.argmax(dmx[np.arange(dmx.shape[0]), np.argmin(dmx, axis=1)])
np.argmin(dmx[19])
all_points_skan[19]
all_points_fiji[27]
all_points_fiji[27] / spacing
all_points_skan[19] / spacing
get_ipython().magic('pinfo csr.skeleton_to_csgraph')
g, idx, deg = csr.skeleton_to_csgraph(skel1, spacing=spacing)
deg[22, 146, 410]
deg[20:25, 144:149, 408:413]
deg[20:26, 144:149, 408:413]
deg[21:28, 144:149, 408:413]
# above: clear difference in the branch point location due to
# cluster of junction points
