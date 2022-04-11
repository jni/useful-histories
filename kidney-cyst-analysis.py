# IPython log file

import numpy as np
from scipy import ndimage as ndi
import napari
from skimage import morphology
from skimage import measure
import pandas as pd

viewer = napari.Viewer()
viewer.open('/Users/jni/Desktop/Cystic\ Index.ome.tif')

labels = viewer.layers['Cystic Index.ome'].data
tissue = (labels == 4)  # found label by inspecting status bar on viewer
layer = viewer.layers['Cystic Index.ome']

squm_per_pixel = 3.9792**2  # found by using ome-types plugin drag-n-drop
pixels_in_1000 = 1000 / squm_per_pixel
pixels_in_1000  # ~64

tissue_plugged = morphology.remove_small_holes(tissue, area_threshold=64)

viewer.add_labels(tissue_plugged)  # just to see how we did
labels[tissue_plugged] = 4  # now fix up original labels
layer.refresh()  # update display as we've updated the labels data

# we used many labels for cysts because they can look quite different.
# but now we want to only distinguish cyst vs non-cyst, so we merge them.
any_cyst = (labels == 1) + (labels == 2) + (labels == 3) + (labels == 5)
labels[any_cyst] = 1
layer.refresh()

# Now we remove the cruft in the background/things that fall outside the slice
# of tissue. These can be seen as "holes" in the background. The tissue itself
# is just one big hole, but it's so big that it will get filtered out by our
# size threshold.
background = (labels == 0)
background_filled = morphology.remove_small_holes(background, 500000)
viewer.add_labels(background_filled)
labels[background_filled] = 0
layer.refresh()

# Now we go from cysts/no cyst to individually-labeled cysts. This is moving
# from *semantic segmentation* (does this pixel belong to a cyst, or not?) to
# *instance segmentation* (does this pixel belong to cyst number 2439?)
individual_cysts = ndi.label(labels == 1)[0]
viewer.add_labels(individual_cysts)
# Note: editing the labels in the layer above with painting or plugins will
# edit the "individual_cysts" array in-place, which we can then use below.


# Now, measure the properties we're interested it
table = pd.DataFrame(measure.regionprops_table(
    individual_cysts, properties=['label', 'area']))
table['area (µm2)'] = table['area'] * squm_per_pixel
table.head()  # first five rows
table.describe()  # statistics about each column
table.to_excel('one-image.xlsx')

# Measure the total area of cysts in this file
cyst_percent = np.sum(labels == 1) / np.sum(labels != 0) * 100
print(cyst_percent)

napari.run()
