import matplotlib.pyplot as plt
import numpy as np
import ligraph3 as lg

def examplefunc(x, y, z, r, phi, theta):
    return np.log(theta + r) - x*np.exp(-z**2) + y - 1

def example():
    b = 9
    
    x0 = -b
    x1 = b
    y0 = -b
    y1 = b
    z0 = -b
    z1 = b
    
    xs, ys, zs = lg.solve3D(examplefunc, x0, x1, y0, y1, z0, z1, N = 300)
    
    lg.mplot3D(xs, ys, zs, x0, x1, y0, y1, z0, z1)

    plt.show()
    
example()