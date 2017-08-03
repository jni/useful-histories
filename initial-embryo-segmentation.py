# IPython log file
import numpy as np
from scipy import ndimage as ndi
from skimage import io, segmentation, filters, feature, morphology
import matplotlib.pyplot as plt

# load in data
droso = io.imread('/Users/jni/Dropbox/data1/drosophila-embryo/E_z2_512_1um_CONTROL.tif') / 4096

# Interpolate to obtain an isotropic volume
rc_scale = 0.248  # Obtained from Fiji
interp_coords = np.mgrid[0:52:rc_scale, 0:320, 0:512]

# Obtain isotropic volume of nuclei channel (channel 0)
nuclei = ndi.map_coordinates(droso[..., 0], interp_coords)

# A.
# Find the centers of nuclei (brightest points in smoothed image)
# to be used as seeds for watershed segmentation
nuclei_smooth = filters.gaussian(nuclei, sigma=3)
centroids = feature.peak_local_max(nuclei_smooth, min_distance=4,
                                   exclude_border=False, indices=False)

# B.
# Use the membrane channel to get isotropic volume to act as boundaries
# for the watershed.
# Sections A and B should be replaced with volumes learned in Ilastik...
seeds, nseeds = ndi.label(centroids)
membranes = ndi.map_coordinates(droso[..., 1], interp_coords)

# Perform watershed segmentation
# Note, this currently takes quite a while, known issue on scikit-image
seg = morphology.watershed(membranes, seeds, compactness=0.01)

# Optional: visualise the segmentation. This is still clunky.
# Uncomment these lines to be able to use the slice viewer
#sys.path.append('/Users/jni/projects/mpl-volume-viewer/')
#import slice_view as sv
#labels = np.arange(nseeds + 1)
#np.random.shuffle(labels)
#colors = plt.cm.spectral(labels[seg]/labels[seg].max())
#viewer = sv.SliceViewer(colors)
#viewer = sv.SliceViewer(np.stack((nuclei, membranes, nuclei), axis=-1))

# Use regionprops to measure properties of the segments
# The resulting list is a little bit counterintuitive: pnuc[i] contains
# the region properties of the i^th non-zero segment. So if you have
# sequential nonzero segments 1, 2, 3, ..., then their properties will be
# at pnuc[0], pnuc[1], pnuc[2], ...
pnuc = measure.regionprops(seg, intensity_image=nuclei)
avg_nuc = [p.mean_intensity for p in pnuc]
# Uncomment this line to see a histogram of nucleus channel intensity
# across segments. We use this measure as a crude estimate of whether
# a segment contains a cell or not
#plt.hist(avg_nuc, bins='auto');
is_cell = [avg_nuc_i > 0.4 for avg_nuc_i in avg_nuc]

# Obtain the central moments. This requires source installation of
# this skimage branch:
# https://github.com/jni/scikit-image/tree/moments3d
seg_moments = [p.moments_central for p in pnuc]

# Define some functions to get orientation from central moments
# These are based on
# https://en.wikipedia.org/wiki/Image_moment
#
# The "cov" matrix defined below may or may not be also known as
# the inertia tensor (based on short inspection of inertia tensor source
# code in scikit-image)
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
    """Return eccentricity and principal direction given a covariance matrix.

    The eccentricity is the ratio of the largest eigenvalue to the second
    largest. In a 3D problem, there is probably some more descriptive shape
    metric that uses all three eigenvalues.
    """
    evals, evecs = np.linalg.eig(covmat)
    sorted_evals = np.argsort(evals)
    ecc = evals[sorted_evals][-1] / evals[sorted_evals][-2]
    return ecc, evecs[:, sorted_evals[-1]]


covmat2direction(mat)
directions = [covmat2direction(moments2cov(m))
              for m in seg_moments]


# To do:
# - improve segmentation
# - plot all the directions. You could use "is_cell" together with
#   [p.centroid for p in pnuc] to draw the principal directions using
#   vpython -- scaled by the eccentricity.
# - find the distribution of eccentricity
# - find the variance of direction between neighbouring cells. This requires
#   the neighbourhood graph.
# - realign cells according to their direction vector, and measure the
#   polarity of the 3rd channel based on that alignment.
