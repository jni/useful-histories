# IPython log file


import napari
import tifffile
import geopandas as gpd
import numpy as np
from shapely.geometry import Polygon, mapping

dsr = tifffile.imread('DSR_Stack.tif')
ndvi = tifffile.imread('NDVI_Stack.tif')
viewer = napari.Viewer()
dsr[dsr < 0] = -1
ndvi = np.nan_to_num(ndvi, nan=-1)
dsr_layer = viewer.add_image(dsr, scale=(1, 1, 1))
ndvi_layer = viewer.add_image(ndvi, scale=(1, 0.25, 0.25))

shapefile = gpd.read_file('/Users/jni/data/geo/ArqAcores_5/ArqAcores_Outline_5_CAOP2019.shp')
shapefeature = shapefile.query("DI == '43'")
polygon = shapefeature.geometry.iloc[0]
polygon_tuple = mapping(polygon)['coordinates']
polygon_array = np.array(polygon_tuple)
island_shape = viewer.add_shapes([np.column_stack([polygon_array[:, 1], polygon_array[:, 0]])], shape_type='polygon', edge_width=0, scale=(-1, 1))
