# IPython log file


import os
import sys
sys.path.append('/Users/jni/projects/unfold-embryo')
sys.path.append('/Users/jni/projects/skan')

from gala import imio
import unfold

os.chdir('/Users/jni/Dropbox/data1/drosophila-embryo/')
v = imio.read_h5_stack('embA_0.3um_Probabilities.h5')
smoothed_vm = filters.gaussian(v[..., 0], sigma=4)
b = (smoothed_vm > 0.5)[::2, ::2, ::2]
b2 = morphology.remove_small_objects(b, 1000)
g, idxs, path = unfold.define_mesoderm_axis(b2)
sources, ids, idxs = unfold.source_id_volume(b2, idxs, path)
c0 = unfold.coord0_volume(sources, idxs)
c1 = unfold.coord1_volume(b2)
image = io.imread('embA_0.3um.tif')[::2, ::2, ::2]
channels = [unfold.sample2d(c0, c1, image[..., c])
            for c in range(3)]
            
