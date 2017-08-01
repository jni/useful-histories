# IPython log file


droso = io.imread('/Users/jni/Dropbox/data1/drosophila-embryo/E_z2_512_1um_CONTROL.tif') / 4096
sys.path.append('/Users/jni/projects/mpl-volume-viewer/')
import slice_view as sv
nuclei = droso[..., 0]
nuclei_smooth = filters.gaussian(nuclei, sigma=[0.6, 3, 3])
centroids = feature.peak_local_max(nuclei_smooth, min_distance=3, exclude_border=False, indices=False)
seeds = ndi.label(centroids)[0]
seeds.max()
seg = morphology.watershed(droso[..., 1], seeds, compactness=0.05)
labels = np.arange(np.max(seg) + 1)
np.random.shuffle(labels)
colors = plt.cm.spectral(labels[seg]/labels[seg].max())
#viewer = sv.SliceViewer(colors, spacing=[5, 1, 1])
