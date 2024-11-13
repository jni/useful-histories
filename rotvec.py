# IPython log file


angles = (-7.458886512670763, 2.8365682364170794, 149.5746701122393)
angle_arr = np.loadtxt('angles.txt', delimiter=',')
get_ipython().run_line_magic('cd', '~/ipython_logs')
get_ipython().run_line_magic('cd', '~/ipython-logs')
angle_arr = np.loadtxt('angles.txt', delimiter=',')
plt.plot(angle_arr.T)
plt.plot(angle_arr)
fig, ax = plt.subplots()
ax.plot(angle_arr)
fig.savefig('/Users/jni/Downloads/figure1.png')
viewer = napari.Viewer(ndisplay=3)
image.shape
image = tifffile.imread('/Users/jni/data/ovarioles/droso-ovarioles-downsampled.tif')
import tifffile 
image = tifffile.imread('/Users/jni/data/ovarioles/droso-ovarioles-downsampled.tif')
viewer.add_image(image)
image.dtype
image.max()
image = image.astype(np.uint8)
viewer = napari.Viewer(ndisplay=3)
viewer.add_image(image)
from scipy import spatial
get_ipython().run_line_magic('pinfo', 'spatial.transform.Rotation.from_rotvec')
r = spatial.transform.Rotation.from_rotvec((1, 0, 0))
r = spatial.transform.Rotation.from_rotvec((1, 0, 0), degrees=True)
viewer.camera.angles
viewer.camera.angles = (0, 0, 150)
viewer.camera.angles = (0, 0, 135)
R = spatial.transform.Rotation
get_ipython().run_line_magic('pinfo', 'R.from_euler')
rcam = R.from_euler(seq='yzx', angles=viewer.camera.angles, degrees=True)
r * rcam
result = r * rcam
result.to_euler(seq='yzx', degrees=True)
result
result.as_euler(seq='yzx', degrees=True)
viewer.camera.angles = (0, 0, 136)
def rotvecify(viewer, vector):
    r = R.from_rotvec(vector, degrees=True)
    rcam = R.from_euler(
            seq='yzx',
            angles=viewer.camera.angles,
            degrees=True,
            )
    result = r * rcam
    angles = result.as_euler(seq='yzx', degrees=True)
    viewer.camera.angles = angles
    return angles
    
viewer.camera.angles = (0, 0, 135)
rotvecify(viewer, (0, 5, 0))
viewer.camera.angles = (0, 0, 135)
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 5))
rotvecify(viewer, (0, 0, 180))
rotvecify(viewer, (0, 0, 90))
rotvecify(viewer, (0, 0, 20))
rotvecify(viewer, (0, 0, 20))
rotvecify(viewer, (0, 0, 20))
def rotvecify(viewer, vector):
    r = R.from_rotvec(vector[::-1], degrees=True)
    rcam = R.from_euler(
            seq='yzx',
            angles=viewer.camera.angles,
            degrees=True,
            )
    result = r * rcam
    angles = result.as_euler(seq='yzx', degrees=True)
    viewer.camera.angles = angles
    return angles
    
rotvecify(viewer, (0, 0, 20))
image.scale
viewer.layers[0].scale
np.asarray(viewer.layers[0].data.shape) / 2
viewer.add_vectors(
    [(68, 296, 395), (-100, 0, 0)]
    )
viewer.camera.up_direction
def rotvecify_sane(viewer, vector_direction, angle):
    vector = np.asarray(vector_direction) / np.linalg.norm(vector_direction)
    return rotvecify(viewer, vector * angle)
    
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
rotvecify_sane(viewer, viewer.camera.up_direction, 20)
viewer.camera.angles
viewer.camera.angles = (0, 0, 135)
rotvecify_sane(viewer, (1, 0, 0), 90)
rotvecify_sane(viewer, (1, 0, 0), -90)
rotvecify_sane(viewer, (1, 0, 0), 90)
viewer.camera.center
get_ipython().run_line_magic('pinfo', 'np.cross')
def angle_from_vecs(a, b):
    dot = np.dot(a, b)
    return np.arccos(dot / np.linalg.norm(a) / np.linalg.norm(b))
    
angle_from_vecs((0, 1, 0), (1, 0, 0))
def angle_from_vecs(a, b):
    dot = np.dot(a, b)
    return np.degrees(np.arccos(dot / np.linalg.norm(a) / np.linalg.norm(b)))
    
angle_from_vecs((0, 1, 0), (1, 0, 0))
angle_from_vecs((0, 1, 0), (1, 1, 0))
angle_from_vecs(viewer.camera.view_direction, (-100, 0, 0))
angle_from_vecs(viewer.camera.view_direction, (100, 0, 0))
viewer.camera.angles = (0, 0, 135)
angle_from_vecs(viewer.camera.view_direction, (100, 0, 0))
viewer.add_points([viewer.camera.center])
viewer.camera.center
viewer.camera.center = (130, 295.5, 394.5)
viewer.camera.angles = (0, 0, 135)
rotvecify_sane(viewer, (1, 0, 0), 90)
viewer.camera.position
