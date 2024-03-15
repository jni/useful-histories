# IPython log file


import napari
viewer = napari.Viewer()
viewer.open('step21.defdap.yml', plugin='napari-defdap')
viewer.open('step21.defdap.yml', plugin='napari-defdap')
viewer.open('step21.defdap.yml', plugin='napari-defdap')
ebsd = viewer.layers[0].metadata['ebsdmap']
type(ebsd.data.euler_angle)
ebsd.data.euler_angle.shape
euler_rgb = np.transpose(ebsd.data.euler_angle, (1, 2, 0)) / [2*np.pi, np.pi/2, np.pi/2]
viewer.layers[1].data.shape
viewer.layers[0].data.shape
viewer.layers[0].scale
np.max(euler_rgb, axis=(0, 1))
viewer.add_image(euler_rgb, rgb=True, scale=viewer.layers[0].scale)
dic = viewer.layers[0].metadata['dicmap']
warped_channels = [dic.warp_to_dic_frame(euler_rgb[..., i], crop_image=True) for i in range(3)]
warped_channels = [dic.warp_to_dic_frame(euler_rgb[..., i], crop=True) for i in range(3)]
euler_rgb2 = np.stack(warped_channels, axis=-1)
viewer.add_image(euler_rgb2, rgb=True, scale=viewer.layers[0].scale)
euler_rgb2.shape
viewer.layers[0].data.shape
viewer.add_image(euler_rgb2[20:, 25:], rgb=True, scale=viewer.layers[0].scale)
viewer.add_image(euler_rgb2[25:, 20:], rgb=True, scale=viewer.layers[0].scale)
viewer.layers[-1].data.shape
viewer.layers[-1].scale = np.asarray(viewer.layers[0].scale) / 3
