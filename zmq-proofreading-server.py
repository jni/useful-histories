# IPython log file


from gala import agglo, serve
import numpy as np
frag = np.loadtxt('test-02-watershed.txt').astype(int)
prob = np.loadtxt('test-02-probabilities.txt')
solver = serve.Solver(frag, prob)
solver.listen()
