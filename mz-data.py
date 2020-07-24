# IPython log file


import numpy as np
import napari
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure


# load the data
cube = np.load('datacube.npy')
peaks = np.load('peaklist.npy')
mz = peaks[0]
thresh = np.load('hsr_thresholds.npy')
cubet = np.transpose(cube, (2, 0, 1))
cubet_norm = cubet / thresh[:, np.newaxis, np.newaxis]


# create qt application context
with napari.gui_qt():
    # create the viewer
    viewer = napari.view_image(cubet_norm)


    # create the intensity plot
    with plt.style.context('dark_background'):
        mz_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        mz_axes = mz_canvas.figure.subplots()
        intensities = cubet[:, 0, 0]
        intensity_line = mz_axes.plot(mz, intensities)[0]  # returns line list
        position_line = mz_axes.axvline(x=mz[0], c='C1')
        position_line.set_zorder(-1)  # keep the spectra in front
        minval, maxval = np.min(cube), np.max(cube)
        range_ = maxval - minval
        centre = (maxval + minval) / 2
        min_y = centre - 1.05 * range_ / 2
        max_y = centre + 1.05 * range_ / 2
        mz_axes.set_ylim(min_y, max_y)
        mz_axes.set_xlabel('m/z')
        mz_axes.set_ylabel('intensity')
        title = mz_axes.set_title(f'coord=(0, 0); m/z={mz[0]:.3f}')
        mz_canvas.figure.tight_layout()


    # add the plot to the viewer
    viewer.window.add_dock_widget(mz_canvas)


    # create a function to update the plot
    def update_plot(axis_event):
        axis = axis_event.axis
        if axis != 0:
            return
        slice_num = axis_event.value
        x = mz[slice_num]
        position_line.set_data([x, x], [0, 1])
        coord_str, mz_str = title.get_text().split(';')
        title.set_text(coord_str + '; ' + f'm/z={x:.3f}')
        mz_canvas.draw_idle()


    # connect the function to the dims axis
    viewer.dims.events.axis.connect(update_plot)


    # grab the image layer
    layer = viewer.layers[0]


    # add a click callback to the layer to update the spectrum being viewed
    @layer.mouse_drag_callbacks.append
    def update_intensity(layer, event):
        xs, ys = intensity_line.get_data()
        coords_full = tuple(np.round(layer.coordinates).astype(int))
        if all(coords_full[i] in range(cubet.shape[i])
                for i in range(cubet.ndim)):
            coords = coords_full[1:]  # rows, columns
            new_ys = cube[coords]
            intensity_line.set_data(xs, new_ys)
            coord_str, mz_str = title.get_text().split(';')
            title.set_text(str(coords) + '; ' + mz_str)
            mz_canvas.draw_idle()

