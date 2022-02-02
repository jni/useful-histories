# IPython log file

from collections import deque
import matplotlib.pyplot as plt
import numpy as np
import dask.array as da
import skan
import napari
import networkx as nx
from scipy import ndimage as ndi
from skimage import morphology
from scipy import spatial

##################################################
# PART ONE: SHOLL ANALYSIS
# https://en.wikipedia.org/wiki/Sholl_analysis
# Count the number of crossings of paths of spherical shells away from a
# central point.
#
# First, get the skeleton and summary using skan

arr = np.asarray(da.from_zarr('bin.zarr'))
filled = ndi.binary_fill_holes(arr)
bin_skeleton = morphology.skeletonize(filled) > 0
scale = (1.0785801681301463, 0.6918881978764917, 0.6918881978764917)
deg_image = skan.csr.make_degree_image(bin_skeleton)
viewer = napari.view_image(deg_image, ndisplay=3)
skel = skan.csr.Skeleton(bin_skeleton, spacing=scale)
summary = skan.summarize(skel)
# see summary.columns for info.

# Now, define the centre pixel in real coordinates
center_pixel = np.asarray([5, 34, 37])
center_pixel_real = center_pixel * scale

# Then, define the shell radii (you can do this however you like, this is
# just one suggestion.)
dataset_radius = np.sqrt(np.sum(
    (np.asarray(bin_skeleton.shape) * scale)**2)) / 2
shell_radii = np.linspace(0, dataset_radius, 15)


# This function takes a path ID, and returns the distance from each pixel in
# the path to the central pixel. (The central pixel must be input in pixel,
# not real, coordinates.)
# Later, we know that if the distances along the path jump across a shell,
# then we can increment the number of crossings of that shell.
def path_distances(skel, center_point, path_id):
    path = skel.path_coordinates(path_id)
    center_point_scaled = skel.spacing * center_point
    path_scaled = path * skel.spacing
    distances = np.ravel(
        spatial.distance_matrix(path_scaled, [center_point_scaled]))
    return distances


# Array to keep track of the crossings
all_crossings = np.zeros_like(shell_radii)

# For each path:
for i in range(skel.n_paths):
    # Find the distances of the path pixels
    distances = path_distances(skel, center_pixel, i)
    # Find which shell bin each pixel sits in
    shell_location = np.digitize(distances, shell_radii)
    # Use np.diff to find where bins are crossed. The -1 accounts for
    # "shell 0" not existing.
    crossings = shell_location[np.flatnonzero(np.diff(shell_location))] - 1
    # increment the corresponding crossings
    all_crossings[crossings] += 1

# Plot the number of crossings at each radius
plt.plot(all_crossings)
plt.show()

###############################################################
# PART TWO:
# finding "depth" of a branch from the soma of a neuron.
# This is standard depth-first-search, but unfortunately networkx DFS doesn't
# report the depth, so we copy the code over.

labels_layer = viewer.add_labels(np.asarray(skel))

# Create a graph from the junctions
junction_graph = nx.Graph()
junction_graph.add_edges_from(
    zip(summary['node-id-src'], summary['node-id-dst']))

# Define the "soma" junction. You probably have better ways of doing this,
# in our case, the center pixel was not actually a junction, so we find the
# nearest junction to the center pixel
coords_junctions = summary[[f'image-coord-src-{i}'
                            for i in range(3)]].to_numpy()
ctr = np.all(coords_junctions == center_pixel, axis=1)
np.flatnonzero(ctr)
distance_from_center = spatial.distance_matrix(coords_junctions,
                                               [center_pixel])
nearest_junction_to_center = np.argmin(distance_from_center)
soma_junction = int(summary.iloc[nearest_junction_to_center]['node-id-src'])

######################################################
# The next two functions are copied from
# https://networkx.org/documentation/stable/_modules/networkx/algorithms/traversal/breadth_first_search.html,
# but have been modified to yield the *depth* as well as the edge ID.


def generic_bfs_edges(G,
                      source,
                      neighbors=None,
                      depth_limit=None,
                      sort_neighbors=None):
    if callable(sort_neighbors):
        _neighbors = neighbors
        neighbors = lambda node: iter(sort_neighbors(_neighbors(node)))

    visited = {source}
    if depth_limit is None:
        depth_limit = len(G)
    queue = deque([(source, depth_limit, neighbors(source))])
    while queue:
        parent, depth_now, children = queue[0]
        try:
            child = next(children)
            if child not in visited:
                yield (parent, child), depth_limit - depth_now + 1
                visited.add(child)
                if depth_now > 1:
                    queue.append((child, depth_now - 1, neighbors(child)))
        except StopIteration:
            queue.popleft()


def bfs_edges(G, source, reverse=False, depth_limit=None, sort_neighbors=None):
    if reverse and G.is_directed():
        successors = G.predecessors
    else:
        successors = G.neighbors
    yield from generic_bfs_edges(G, source, successors, depth_limit,
                                 sort_neighbors)


# this gives a list of edges as node-id pairs, together with depth.
# you will need to match the node-id pairs to rows in the summary table.
# then, you can add a column to the dataframe, e.g., 'depth-from-soma', and
# finally colour by that value as shown in vessel-skeleton-analysis.py
edges = list(bfs_edges(junction_graph, source=soma_junction))
print(edges[:10])

napari.run()
