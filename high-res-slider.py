import functools
import numpy as np
import dask.array as da
from magicgui.widgets import Slider, Container
import napari

# stack = ...  # your dask array
# stack2 = stack[::2, ::2, ::2]
# stack4 = stack2[::2, ::2, ::2]
# 👆 quick and easy multiscale pyramid, don't do this really
# see https://github.com/dask/dask-image/issues/136
# for better ways
# and, specifically, stack4 will be small but will still need
# to access full data. You should save all data sizes as
# their own arrays on disk and load those. I recommend
# using dask.array.Array.to_zarr.
# You can also read about NGFF:
# https://ngff.openmicroscopy.org/latest/

# example with some example data from Liu et al, Science, 2018

stack, stack2, stack4 = [
    da.from_zarr(f'/Users/jni/data/gokul-lls/{i}.zarr')[0]
    for i in range(3)
]

# a list of arrays of decreasing size is interpreted as
# a multiscale dataset by napari
multiscale_data = [stack, stack2, stack4]

viewer = napari.Viewer(ndisplay=3)
multiscale_layer = viewer.add_image(
    multiscale_data,
    colormap='magenta',
    scale=[3, 1, 1],
)

crop_sizes = (30, 256, 256)
cropz, cropy, cropx = crop_sizes
shapez, shapey, shapex = stack.shape
ends = np.asarray(stack.shape) - np.asarray(crop_sizes) + 1
stepsizes = ends // 100

highres_crop_layer = viewer.add_image(
    stack[:cropz, :cropy, :cropx],
    name='cropped',
    blending='additive',
    colormap='green',
    scale=multiscale_layer.scale,
)

def set_slice(axis, value):
    idx = int(value)
    scale = np.asarray(highres_crop_layer.scale)
    translate = np.asarray(highres_crop_layer.translate)
    izyx = translate // scale
    izyx[axis] = idx
    i, j, k = izyx
    highres_crop_layer.data = stack[i:i + cropz, j:j + cropy, k:k + cropx]
    highres_crop_layer.translate = scale * izyx
    highres_crop_layer.refresh()


sliders = [
    Slider(name=axis, min=0, max=end, step=step)
    for axis, end, step in zip('zyx', ends, stepsizes)
]
for axis, slider in enumerate(sliders):
    slider.changed.connect(
        lambda event, axis=axis: set_slice(axis, event.value)
    )

container_widget = Container(layout='vertical')
container_widget.extend(sliders)
viewer.window.add_dock_widget(container_widget, area='right')

napari.run()
