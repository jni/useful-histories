# IPython log file


from skimage.external import tifffile
import napari
import zipfile


#napari.view_image(arr, contrast_limits=[0, 2**16-1], is_pyramid=False)
f = zipfile.ZipFile('/home/jni/data/francois/SENTINEL2B_20180806-001625-547_L2A_T55HCU_C_V1-0.zip')
# print(f.filelist)
tiff_zip = f.open('SENTINEL2B_20180806-001625-547_L2A_T55HCU_C_V1-0/SENTINEL2B_20180806-001625-547_L2A_T55HCU_C_V1-0_SRE_B12.tif')
tiff = tifffile.TiffFile(tiff_zip)
tiff_zip2 = f.open('SENTINEL2B_20180806-001625-547_L2A_T55HCU_C_V1-0/SENTINEL2B_20180806-001625-547_L2A_T55HCU_C_V1-0_SRE_B8.tif')
tiff2 = tifffile.TiffFile(tiff_zip2)
with napari.gui_qt():
    print(tiff.pages[0].shape)
    print(tiff2.pages[0].shape)
    v = napari.view_image(tiff.pages[0].asarray(), scale=[20, 20], name='SRE_B12')
    v.add_image(tiff.pages[0].asarray(), scale=[10, 10], name='SRE_B8')
