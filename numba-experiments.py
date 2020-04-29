# IPython log file
# cd ~/projects/play
# make sure cache.py is around


get_ipython().run_line_magic('run', '-i cache.py')
_correlate_sparse_offsets.inspect_types()
_correlate_sparse_offsets.inspect_types(pretty=True)
get_ipython().run_line_magic('run', '-i cache.py')
get_ipython().run_line_magic('pinfo', '_correlate_sparse_offsets.inspect_types')
_correlate_sparse_offsets.inspect_types()
import numpy as np
from numba import jit
def find_instr(func, keyword, sig=0, limit=5):
    count = 0
    for l in func.inspect_asm(func.signatures[sig]).split('\n'):
        if keyword in l:
            count += 1
            print(l)
            if count >= limit:
                break
    if count == 0:
        print('No instructions found')
        
@jit(nopython=True)
def sqdiff(x, y):
    out = np.empty_like(x)
    for i in range(x.shape[0]):
        out[i] = (x[i] - y[i])**2
    return out
    
x32 = np.linspace(1, 2, 10000, dtype=np.float32)
y32 = np.linspace(2, 3, 10000, dtype=np.float32)
sqdiff(x32, y32)
x64 = x32.astype(np.float64)
y64 = y32.astype(np.float64)
sqdiff(x64, y64)
sqdiff.signatures
get_ipython().run_line_magic('timeit', 'sqdiff(x32, y32)')
get_ipython().run_line_magic('timeit', 'sqdiff(x64, y64)')
print('float32:')
find_instr(sqdiff, keyword='subp', sig=0)
print('---\nfloat64:')
find_instr(sqdiff, keyword='subp', sig=1)
@jit(nopython=True)
def frac_diff1(x, y):
    out = np.empty_like(x)
    for i in range(x.shape[0]):
        out[i] = 2 * (x[i] - y[i]) / (x[i] + y[i])
    return out
    
frac_diff1(x32, y32)
find_instr(frac_diff1, keyword='subp', sig=0)
@jit(nopython=True, error_model='numpy')
def frac_diff2(x, y):
    out = np.empty_like(x)
    for i in range(x.shape[0]):
        out[i] = 2 * (x[i] - y[i]) / (x[i] + y[i])
    return out
    
frac_diff2(x32, y32)
find_instr(frac_diff2, keyword='subp', sig=0)
frac_diff2(x64, y64)
get_ipython().run_line_magic('timeit', 'frac_diff2(x32, y32)')
get_ipython().run_line_magic('timeit', 'frac_diff2(x64, y64)')
frac_diff2.inspect_types(pretty=True)
@jit(nopython=True, error_model='numpy')
def frac_diff3(x, y):
    out = np.empty_like(x)
    dt = x.dtype # Cast the constant using the dtype of the input
    for i in range(x.shape[0]):
        # Could also use np.float32(2) to always use same type, regardless of input
        out[i] = dt.type(2) * (x[i] - y[i]) / (x[i] + y[i])
    return out
    
frac_diff3(x32, y32)
frac_diff3(x64, y64)
get_ipython().run_line_magic('timeit', 'frac_diff3(x32, y32)')
get_ipython().run_line_magic('timeit', 'frac_diff3(x64, y64)')
SQRT_2PI = np.sqrt(2 * np.pi)

@jit(nopython=True, error_model='numpy', fastmath=True)
def kde(x, means, widths):
    '''Compute value of gaussian kernel density estimate.
    
    x - location of evaluation
    means - array of kernel means
    widths - array of kernel widths
    '''
    n = means.shape[0]
    acc = 0.
    for i in range(n):
        acc += np.exp( -0.5 * ((x - means[i]) / widths[i])**2 ) / widths[i]
    return acc / SQRT_2PI / n
    


@jit(nopython=True)
def sqdiff_indirect(x, y, indirection):
    out = np.empty_like(x)
    for i in range(x.shape[0]):
        out[indirection[i]] = (x[indirection[i]] - y[indirection[i]])**2
    return out

indirection = np.arange(x32.size)

get_ipython().run_line_magic('timeit', 'sqdiff_indirect(x32, y32, indirection)')
get_ipython().run_line_magic('timeit', 'sqdiff_indirect(x64, y64, indirection)')

print('float32:')
find_instr(sqdiff_indirect, keyword='subp', sig=0)
print('---\nfloat64:')
find_instr(sqdiff_indirect, keyword='subp', sig=1)

get_ipython().run_line_magic('run', '-i cache.py')
get_ipython().run_line_magic('run', '-i cache.py')
get_ipython().run_line_magic('run', '-i cache.py')
find_instr(_correlate_sparse_offsets, keyword='subp', sig=0)
get_ipython().run_line_magic('run', '-i cache.py')
get_ipython().run_line_magic('run', '-i cache.py')
find_instr(_correlate_sparse_offsets, keyword='subp', sig=0)
_correlate_sparse_offsets.inspect_types()
get_ipython().run_line_magic('run', '-i cache.py')
get_ipython().run_line_magic('run', '-i cache.py')
find_instr(_correlate_sparse_offsets, keyword='subp', sig=0)
find_instr(_correlate_sparse_offsets, keyword='mulp', sig=0)
find_instr(_correlate_sparse_offsets, keyword='p', sig=0)
find_instr(_correlate_sparse_offsets, keyword='pd', sig=1)
find_instr(_correlate_sparse_offsets, keyword='pd', sig=0)
find_instr(_correlate_sparse_offsets, keyword='pf', sig=1)
find_instr(_correlate_sparse_offsets, keyword='ps', sig=1)
get_ipython().run_line_magic('run', '-i cache.py')
get_ipython().run_line_magic('run', '-i cache.py')
find_instr(_correlate_sparse_offsets, keyword='pd', sig=0)
find_instr(_correlate_sparse_offsets, keyword='ps', sig=1)
_correlate_sparse_offsets.inspect_asm
_correlate_sparse_offsets.inspect_asm()
get_ipython().run_line_magic('pinfo', '_correlate_sparse_offsets.inspect_asm')
_correlate_sparse_offsets.inspect_asm(0)
q
_correlate_sparse_offsets.inspect_asm()[0]
_correlate_sparse_offsets.inspect_asm().keys()
print(list(_correlate_sparse_offsets.inspect_asm().values())[0])
