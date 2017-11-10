# IPython log file


from sklearn.cluster import DBSCAN
x = np.array([5, 8, 10])
5 < x < 11
np.all(5 < x < 11)
get_ipython().run_line_magic('pinfo', 'np.round')
import collections
get_ipython().run_line_magic('pinfo', 'collections.namedtuple')
get_ipython().run_line_magic('pinfo', 'np.percentile')
get_ipython().run_line_magic('pinfo', 'np.percentile')
get_ipython().run_line_magic('pwd', '')
import sys
sys.path.append('/Users/jni/projects/storm-cluster/')
import stormcluster as sc
loc_table = sc.read_locations_table('EXP1_KAHRP_04_405_01_LDCTracked.txt')
loc_table = sc.read_locations_table('30hrTr_KAHRP647mMESA488r_003_405_01_LDCTracked.txt')
loc_table.head()
image = sc.image_from_table(loc_table)
get_ipython().run_line_magic('pdb', '')
image = sc.image_from_table(loc_table)
reload(sc)
image = sc.image_from_table(loc_table)
reload(sc)
image = sc.image_from_table(loc_table)
reload(sc)
image = sc.image_from_table(loc_table)
reload(sc)
image = sc.image_from_table(loc_table)
reload(sc)
image = sc.image_from_table(loc_table)
plt.imshow(image)
from matplotlib.widgets import RectangleSelector
get_ipython().run_line_magic('pinfo', 'RectangleSelector')
fig, ax = plt.subplots()
ax.imshow(image)
RectangleSelector(ax)
get_ipython().run_line_magic('pinfo', 'RectangleSelector')
reload(sc)
sc.select_roi(image)
reload(sc)
sc.select_roi(image)
reload(sc)
sc.select_roi(image)
_
reload(sc)
sc.select_roi(image)
reload(sc)
sc.select_roi(image)
round(45.9)
reload(sc)
rois = sc.select_roi(image)
rois
type(round(48.9))
reload(sc)
rois = sc.select_roi(image)
rois
reload(sc)
rois = sc.select_roi(image)
rois
reload(sc)
rois = sc.select_roi(image)
rois
reload(sc)
coords = np.stack(sc.image_coords(location_table), axis=1)
coords = np.stack(sc.image_coords(loc_table), axis=1)
coords.shape
coords_roi = coords[sc._in_range(coords[:, 0], rois[0]) &
                    sc._in_range(coords[:, 1], rois[1])]
                    
coords_roi = coords[sc._in_range(coords[:, 0], rois[0][0]) &
                    sc._in_range(coords[:, 1], rois[0][1])]
                    
reload(sc)
reload(sc)
scan = cluster(coords_roi, radius=0.5, core_size=20)
scan = sc.cluster(coords_roi, radius=0.5, core_size=20)
labels, sizes, hist = analyse_clustering(scan, coords_roi)
labels, sizes, hist = sc.analyse_clustering(scan, coords_roi)
roi = rois[0]
roi
plt.imshow(image[slice(*roi[0]), slice(*roi[1])], cmap='magma')
reload(sc)
_ = sc.analyse_clustering(sc.cluster(coords_roi, radius=0.5, core_size=10))
reload(sc)
c = sc.cluster(coords_roi, radius=0.5, core_size=10)
clusterim = sc.image_from_clustering(c, coords_roi, roi)
plt.imshow(clusterim)
reload(sc)
num_clustered, largest_cluster = sc.parameter_scan_image(coords_roi)
reload(sc)
num_clustered, largest_cluster = sc.parameter_scan_image(coords_roi)
plt.imshow(num_clustered)
fig, ax = plt.subplots(1, 2)
ax[0].imshow(num_clustered); ax[1].imshow(largest_cluster)
ax[0].imshow(largest_cluster / (num_clustered + 1))
scan = sc.cluster(coords_roi, radius=3.2, core_size=6)
_ = sc.analyse_clustering(scan)
clusterim = sc.image_from_clustering(scan, coords_roi, roi)
plt.imshow(clusterim)
clusters, sizes, (bins, counts) = sc.analyse_clustering(scan)
plt.figure()
plt.plot(bins, counts)
bins[0]
large_clusters = sizes > 300
np.any(scan.labels_ == 0)
reload(sc)
clusterim = sc.image_from_clustering(scan, coords_roi, roi, size_threshold=300)
plt.imshow(clusterim)
reload(sc)
clusterim = sc.image_from_clustering(scan, coords_roi, roi, size_threshold=300)
plt.imshow(clusterim)
plt.imshow(clusterim[:, :, 1], cmap='magma')
plt.imshow(clusterim[:, :, 1], cmap='magma')
reload(sc)
clusterim = sc.image_from_clustering(scan, coords_roi, roi, size_threshold=300)
plt.imshow(clusterim[:, :, 1], cmap='magma')
plt.imshow(clusterim)
image.shape
plt.imshow(image, cmap='magma')
rois2 = sc.select_roi(image)
fig, ax = plt.subplots(1, 2)
fig, ax = plt.subplots(1, 3)
ax[0].imshow(num_clustered); ax[1].imshow(largest_cluster)
ax[1].imshow(largest_cluster / (num_clustered + 1))
ax[0].imshow(num_clustered); ax[1].imshow(largest_cluster)
ax[2].imshow(largest_cluster / (num_clustered + 1))
