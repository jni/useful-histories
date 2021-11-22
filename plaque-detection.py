# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tifffile 
data = tifffile.imread('/home/veronika/Documents/Plaques_crop_test.tif')
data.shape
data.dtype
import napari
viewer = napari.view_image(data)
from skimage import filters, morphology, measure
threshold = filters.threshold_otsu(data)
thresholded = data>threshold
viewer.add_labels(thresholded)
from scipy import ndimage as ndi
labelled = ndi.label(thresholded)[0]
import numpy as np
sizes = np.bincount(labelled.reshape(-1))
len(sizes)
import matplotlib.pyplot as plt
#plt.hist(sizes, bins='auto')



counts, bins = np.histogram(sizes, bins='auto')
counts[:6],bins[:7]
np.max(sizes)
np.max(sizes[1:])
import pandas as pd
large_only = morphology.remove_small_objects(labelled,50)
fraction_volume = np.sum(large_only>0)/large_only.size
fraction_volume
results_table = pd.DataFrame(measure.regionprops_table(large_only,data,properties = ('label','centroid','mean_intensity','max_intensity','area')))
points_layer = viewer.add_points(results_table[['centroid-0', 'centroid-1', 'centroid-2']],properties=results_table)
points_layer.face_color='area'
results_table.to_csv('napari_output.csv')
napari.run()
