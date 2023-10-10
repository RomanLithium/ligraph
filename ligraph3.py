import matplotlib.pyplot as plt
from numpy import sqrt, arctan2, linspace, newaxis, abs, sort, cbrt, min, power

# GENERAL FUNCTIONS
#
# (xmin, xmax)  - x range
# (ymin, ymax)  - y range
# (zmin, zmax)  - z range
#
# focus         - parameter for thickness. Don't specify for autofocusing
# N             - grid number. 500 points per dimention if not specified
#
# show_progress - 'yes' if progressbar is needed
#
# 2D function template: func(x, y, r, phi)
# 3D function template: func(x, y, z, r, phi, theta)
#
def solve2D(func, xmin = -1., xmax = 1., ymin = -1., ymax = 1., focus = -1, N = 500, show_progress = ''):
    #creating grid with number of points = N
    xs = linspace(xmin, xmax, num = N)[:, newaxis] 
    ys = linspace(ymin, ymax, num = N)
    
    #calculating values on the grid
    gen = abs(func(xs, ys, rg(xs, ys), phig(xs, ys)))
    
    #adjusting the focus if it's not specified
    if focus < 0:
        focus = focusing(gen, 3, 2)
    
    #filtering points where |func - 0| < focus
    points = putpot(gen, xs, ys, focus)
    
    #calculating minimal distance between clusters
    cell = sqrt(((xmax - xmin)/N)**2 + ((ymax - ymin)/N)**2)
    difractor = 5*cell
    
    #clustering and packing points into lists of lists
    xs, ys = pack(points, difractor, show_progress)
    
    return xs, ys

def solve3D(func, xmin = -1., xmax = 1., ymin = -1., ymax = 1., zmin = -1., zmax = 1., focus = -1., N = 50):
    #creating grid with number of points = N
    xs = linspace(xmin, xmax, num = N)[:, newaxis, newaxis]
    ys = linspace(ymin, ymax, num = N)[:, newaxis]
    zs = linspace(zmin, zmax, num = N)
    
    #calculating values on the grid
    gen = abs(func(xs, ys, zs, r(xs, ys, zs), phi(xs, ys, zs), theta(xs, ys, zs)))
    
    #adjusting the focus if it's not specified
    if focus < 0:
        focus = focusing(gen, 10, 3)
        
    return putpot3d(gen, xs, ys, zs, focus)

########################################################################################################################

# auxiliary functions for quick plot
#
# xs, ys, zs   - packs of lists of point coordinates. The size of each list in a pair (xs[o], ys[o])
#                must be shared inside the pair, but may be individual for each pair
#
# color        - the color
# colormap     - 3D-colormap
#
# (xmin, xmax) - x range
# (ymin, ymax) - y range
# (zmin, zmax) - z range
#
def mplot2D(xs, ys, color = 'blue', xmin = -1., xmax = 1., ymin = -1., ymax = 1.):
    for o in range(len(xs)):
        plt.plot(xs[o], ys[o], color)
    axis('square')
    xlim(xmin, xmax)
    ylim(ymin, ymax)
    
def mplot3D(xs, ys, zs, colormap = plt.get_cmap('hot'), xmin = -1., xmax = 1., ymin = -1., ymax = 1., zmin = -1., zmax = 1.):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.set_box_aspect([1, 1, 1])
    ax.scatter3D(xs, ys, zs, cmap = colormap)

########################################################################################################################
    
def rg(x, y):
    return sqrt(x*x + y*y)

def phig(x, y):
    ret = arctan2(y, x)
    return ret

def r(x, y, z):
    return sqrt(x**2 + y**2 + z**2)

def phi(x, y, z):
    return arctan2(y, x)

def theta(x, y, z):
    rho = sqrt(x**2 + y**2)
    return arctan2(rho, z)

########################################################################################################################

def putpot(gen, xs, ys, eps):
    X = []
    for o in range(xs.size):
        for e in range(ys.size):
            if abs(gen[o, e]) < eps:
                X.append([xs[o], ys[e]])
    return X

def putpot3d(gen, xs, ys, zs, focus):
    Xs = []
    Ys = []
    Zs = []
    for o in range(xs.size):
        for e in range(ys.size):
            for a in range(zs.size):
                if abs(gen[o, e, a]) < focus:
                    Xs.append(xs[o])
                    Ys.append(ys[e])
                    Zs.append(zs[a])
    return Xs, Ys, Zs

def focusing(gen, k, dim):
    L = gen.size
    trig = int(power(L, 1/dim))
    return sort(gen.copy('C').flatten('C'))[k*trig]

def pack(X, difractor, show_progress):
    ret = [X[0]]
    patient = X.copy()
    L = len(patient)
    patient.pop(0)
    
    brakes = [0]
    
    for o in range(L - 1):
        dists = []
        for e in range(L-1-o):
            dists.append((ret[o][0] - patient[e][0])**2 + (ret[o][1] - patient[e][1])**2)
        i = dists.index(min(dists))
        if dists[i] > difractor:
            brakes.append(o+1)
        ret.append(patient[i])
        patient.pop(i)
        
        if show_progress == 'yes':
            print(str(o+1) + '/' + str(L))
    
    N = len(brakes) - 1
    xs = [[] for o in range(N)]
    ys = [[] for o in range(N)]
    
    for o in range(N):
        for e in range(brakes[o+1] - brakes[o]):
            xs[o].append(ret[brakes[o] + e][0])
            ys[o].append(ret[brakes[o] + e][1])
        
    return xs, ys
