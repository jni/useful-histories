# IPython log file
import numpy as np
from IPython import get_ipython

from numba import cuda
cuda.detect()
n = int(1e6)
a = np.random.rand(n)
b = np.random.rand(n)
out = np.zeros_like(a)
@cuda.jit
def add_gpu(a, b, out):
    i = cuda.threadIdx.x
    if i < a.size:
        out[i] = a[i] + b[i]
        
get_ipython().magic('timeit -r 1 -n 1 add_cuda[1, n](a, b, out)')
get_ipython().magic('timeit -r 1 -n 1 add_gpu[1, n](a, b, out)')
n = int(1e6)
n = int(1e3)
a = np.random.rand(n)
b = np.random.rand(n)
out = np.zeros_like(a)
get_ipython().magic('timeit -r 1 -n 1 add_gpu[1, n](a, b, out)')
get_ipython().magic('timeit -r 1 -n 1 add_gpu[1, n](a, b, out)')
np.all(out == a+b)
get_ipython().magic('timeit -r 1 -n 1 a + b')
cuda.blockDim
from numba import vectorize
import math

@vectorize(['float32(float32, float32, float32)',
            'float64(float64, float64, float64)'],
           target='cuda')
def cu_discriminant(a, b, c):
    return math.sqrt(b**2 - 4*a*c)
N = 1e4
t = np.float32
get_ipython().magic('pinfo np.random.sample')
A = np.random.sample(N).astype(t)
N = int(1e4)
A = np.random.sample(N).astype(t)
B = np.random.sample(N).astype(t) + 10
C = np.random.sample(N).astype(t)
get_ipython().magic('timeit -r 1 -n 1 D = cu_discriminant(A, B, C)')
get_ipython().magic('timeit -r 1 -n 1 D = cu_discriminant(A, B, C)')
get_ipython().magic('timeit -r 1 -n 1 np.sqrt(B**2 - 4*A*C)')
N = int(1e6)
A = np.random.sample(N).astype(t)
B = np.random.sample(N).astype(t) + 10
C = np.random.sample(N).astype(t)
get_ipython().magic('timeit -r 1 -n 1 D = cu_discriminant(A, B, C)')
get_ipython().magic('timeit -r 1 -n 1 np.sqrt(B**2 - 4*A*C)')
N = int(1e8)
A = np.random.sample(N).astype(t)
B = np.random.sample(N).astype(t) + 10
C = np.random.sample(N).astype(t)
get_ipython().magic('timeit -r 1 -n 1 np.sqrt(B**2 - 4*A*C)')
get_ipython().magic('timeit -r 1 -n 1 D = cu_discriminant(A, B, C)')
N = int(1e8)
N = int(1e7)
A = np.random.sample(N).astype(t)
B = np.random.sample(N).astype(t) + 10
C = np.random.sample(N).astype(t)
get_ipython().magic('timeit -r 1 -n 1 D = cu_discriminant(A, B, C)')
get_ipython().magic('timeit -r 1 -n 1 np.sqrt(B**2 - 4*A*C)')
get_ipython().magic('timeit -r 1 -n 1 D = cu_discriminant(A, B, C)')
get_ipython().magic('timeit -r 1 -n 1 D = cu_discriminant(A, B, C)')
@vectorize(['float32(float32, float32, float32)',
            'float64(float64, float64, float64)'],
           target='cuda')
def cu_crazy_func(a, b, c):
    return math.sqrt(b**2 - 4*math.log(a)*math.sin(c)) + b
    
get_ipython().magic('timeit -r 1 -n 1 np.sqrt(B**2 - 4*np.log(A)*np.sin(C)) + B')
get_ipython().magic('timeit -r 1 -n 1 D = cu_crazy_func(A, B, C)')
get_ipython().magic('timeit -r 1 -n 1 D = cu_crazy_func(A, B, C)')
cuda.detect()
cuda.config()
from skimage import util
get_ipython().magic('pinfo util.apply_parallel')
image = np.random.rand(4096, 4096)
from skimage import filters
get_ipython().magic('timeit g = util.apply_parallel(filters.gaussian, image,')
get_ipython().magic("timeit -r 1 -n 1 g = util.apply_parallel(filters.gaussian, image, chunks=1024, extra_arguments={'sigma': 5})")
import toolz as tz
gauss = tz.curry(filters.gaussian)
get_ipython().magic('timeit -r 1 -n 1 g = util.apply_parallel(gauss(sigma=5), image, chunks=1024)')
get_ipython().magic('timeit -r 1 -n 1 gauss(sigma=5)(image)')
