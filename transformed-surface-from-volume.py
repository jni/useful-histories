import itertools
import numpy as np
import napari


def triangulate_matrix(values):
    r"""Regular triangulation of a matrix, one vertex per coordinate/index.

    Produces a triangulation with the shape:

        (0, 0) -- (0, 1) -- (0, 2) ...
          |   \     |   \     |
          |    \    |    \    |
          |     \   |     \   |
          |      \  |      \  |
        (1, 0) -- (1, 1) -- (1, 2) ...
          ⋮         ⋮          ⋮

    Parameters
    ----------
    values : (M, N) array
        The input array.

    Returns
    -------
    vertices : (M*N, 2) array
        The coordinates of the input array.
    triangles : (P, 3) array of int
        Triangles specified as (i, j, k) triplets of indices into `vertices`.
        The number of triangles is ``2 * (M-1) * (N-1)``.
    """
    shp = values.shape
    ntriangles = 2 * (shp[0] - 1) * (shp[1] - 1)
    triangles = np.zeros((ntriangles, 3), dtype=np.intp)

    # idxs is the linear index into each coordinate on the array
    idxs = np.arange(values.size).reshape(shp)
    # … which we can convert to a coordinate with np.unravel_index
    vertices = np.transpose(np.unravel_index(idxs.ravel(), shp, order='C'))

    # we create offset index arrays with offsets (0, 0), (0, 1), (1, 0),
    # and (1, 1), which we can use to build our triangles
    slices = [slice(0, -1), slice(1, None)]
    tris = [idxs[slc0, slc1].reshape((-1, 1))
            for slc0, slc1 in itertools.product(slices, repeat=2)]

    # then we stack these together to make the triangles. First, the offsets
    # (0, 0), (0, 1), (1, 1)
    _ = np.concatenate(  # up triangles
        [tris[0], tris[1], tris[3]], axis=1, out=triangles[:ntriangles // 2]
    )
    # then, the offsets (0, 0), (1, 1), (1, 0)
    _ = np.concatenate(  # down triangles
        [tris[0], tris[3], tris[2]], axis=1, out=triangles[ntriangles // 2:]
    )

    return vertices, triangles


def volume_surface(
        vol : np.ndarray
        ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Convert a volume of values to a triangulated surface.

    Only the values on the surface of the volume are taken into account.

    The output of this function is suitable for input to a napari
    Surface layer.

    Parameters
    ----------
    vol : 3D array of values
        The volume to be rendered.

    Returns
    -------
    vertices : (N, 3) array of float
        The vertex coordinates of the triangles on the surface of the
        volume.
    triangles : (M, 3) array of int
        (i, j, k) triplets of vertex indices specifying triangles.
    values : (N,) array of float
        The image value at a given vertex.
    """
    # strategy: we are going to treat each face of the volume separately,
    # then concatenate them together; for each dimension, we triangulate the
    # "top" and "bottom" faces separately -- so the loop is executed 6 times.
    shp = vol.shape
    vertices = []
    triangles = []
    values = []
    nvertex = 0  # the current number of vertices
    for fixed_dim in range(3):
        for val in (0, shp[fixed_dim] - 1):
            # get the current volume face values array
            idx = [slice(None),] * 3
            idx[fixed_dim] = val
            values_i = vol[tuple(idx)]

            # get vertices and triangles for the current face (2D)
            vertices_i_raw, triangles_i = triangulate_matrix(values_i)

            # insert back the current face coordinate (back-project to 3D)
            vertices_i = np.insert(vertices_i_raw, fixed_dim, val, axis=1)

            # offset the triangle indices based on the total number of vertices
            # created over all past faces, then add the current count
            triangles_i += nvertex
            nvertex += len(vertices_i)

            # add all the arrays to the total  list
            vertices.append(vertices_i)
            triangles.append(triangles_i)
            values.append(values_i.ravel())

    # concatenate the resulting arrays
    vertices, triangles, values = map(
            np.concatenate, (vertices, triangles, values)
            )

    return vertices, triangles, values


def volume_to_cylinder(
        shape, inner_radius, thickness, degrees, height, coords
        ):
    """Map numpy volume coordinates to a cylinder.

    https://forum.image.sc/t/how-to-visualize-semi-cylindrical-3d-data-in-napari/118252

    This function maps the volume to a "thick" border of a cylinder along
    a certain arc.

    Parameters
    ----------
    shape : 3-tuple of int
        The shape of the volume.
    inner_radius : float
        The radius of the inside of the cylinder.
    thickness : float
        The thickness of the cylinder wall.
    degrees : float
        The number of degrees spanned by the arc of the cylinder.
    height : float
        The height of the cylinder.
    coords : array of float, (N, 3)
        The coordinates to be transformed.

    Returns
    -------
    coords_tf : array of float, (N, 3)
        The transformed coordinates.
    """
    coords = (coords / (np.array(shape) - 1)).T  # map to [0, 1] i, j, k
    new_coords = np.empty(coords.shape, dtype=np.float32)

    # convert k to angle
    theta = coords[2] * np.radians(degrees)
    # convert j to radial distance
    r = coords[1] * thickness + inner_radius
    # convert i to height
    h = coords[0] * height

    # convert cylindrical coordinates to xyz
    new_coords[0] = r * np.cos(theta)
    new_coords[1] = r * np.sin(theta)
    new_coords[2] = h

    # return coordinates as (N, 3) array
    return new_coords.T


if __name__ == '__main__':
    # example from https://forum.image.sc/t/how-to-visualize-semi-cylindrical-3d-data-in-napari/118252
    # converted to napari surfaces
    shp = (388, 200, 2490)
    data = np.random.randint(0, 255, dtype=np.uint8, size=shp)

    # first, create the surface mesh from the data
    vertices, triangles, values = volume_surface(data)

    # next, we transform the vertices to cylindrical coordinates as in the
    # example

    R_inner = 180.0  # mm (inner radius)
    thickness = 15.0  # mm
    theta_span_deg = 180  # half-pipe
    height = 315  # mm

    vertices_tf = volume_to_cylinder(
            shp,
            inner_radius=R_inner, thickness=thickness,
            degrees=theta_span_deg, height=height,
            coords=vertices
            )

    viewer = napari.Viewer(ndisplay=3)
    surf = viewer.add_surface(
            (vertices_tf, triangles, values), colormap='viridis'
            )
    viewer.camera.angles = (-25, 25, 135)  # using https://github.com/napari/napari/pull/8281

    napari.run()