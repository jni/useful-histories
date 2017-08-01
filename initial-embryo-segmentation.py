# IPython log file


droso = io.imread('/Users/jni/Dropbox/data1/drosophila-embryo/E_z2_512_1um_CONTROL.tif') / 4096
sys.path.append('/Users/jni/projects/mpl-volume-viewer/')
import slice_view as sv
labels = np.arange(np.max(seg) + 1)
np.random.shuffle(labels)
colors = plt.cm.spectral(labels[seg]/labels[seg].max())
#viewer = sv.SliceViewer(colors, spacing=[5, 1, 1])
rc_scale = 0.248  # Obtained from Fiji
interp_coords = np.mgrid[0:52:rc_scale, 0:320, 0:512]
nuclei = ndi.map_coordinates(droso[..., 0], interp_coords)
nuclei_smooth = filters.gaussian(nuclei, sigma=3)
centroids = feature.peak_local_max(nuclei_smooth, min_distance=4,
                                   exclude_border=False, indices=False)

seeds, nseeds = ndi.label(centroids)
membranes = ndi.map_coordinates(droso[..., 1], interp_coords)
seg = morphology.watershed(membranes, seeds, compactness=0.01)

labels = np.arange(nseeds + 1)
np.random.shuffle(labels)
colors = plt.cm.spectral(labels[seg]/labels[seg].max())
#viewer = sv.SliceViewer(colors)
#viewer = sv.SliceViewer(np.stack((nuclei, membranes, nuclei), axis=-1))

pnuc = measure.regionprops(seg, intensity_image=nuclei)
avg_nuc = [p.mean_intensity for p in pnuc]
plt.hist(avg_nuc, bins='auto');
is_cell = [avg_nuc_i > 0.4 for avg_nuc_i in avg_nuc]

seg_moments = [p.moments_central for p in pnuc]

def matidx2momentsidx(ndim, idx):
    coords = [0] * ndim
    for i in idx:
        coords[i] += 1
    return tuple(coords)

def moments2cov(moments):
    m0 = moments.ravel()[0]
    ndim = moments.ndim
    cov = np.empty((ndim, ndim))
    for idx in np.ndindex(*cov.shape):
        cov[idx] = moments[matidx2momentsidx(ndim, idx)] / m0
    return cov

def covmat2direction(covmat):
    evals, evecs = np.linalg.eig(covmat)
    sorted_evals = np.argsort(evals)
    ecc = evals[sorted_evals][-1] / evals[sorted_evals][-2]
    return ecc, evecs[:, sorted_evals[-1]]

covmat2direction(mat)
directions = [covmat2direction(moments2cov(m))
              for m in seg_moments]



