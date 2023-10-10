from matplotlib.pyplot import plot, axis, xlim, ylim
from numpy import sqrt, arctan2, linspace, newaxis, abs, sort

# GENERAL FUNCTION
#
# (xmin, xmax)  - x range
# (ymin, ymax)  - y range
#
# focus         - parameter for thickness. Don't specify for autofocusing
# N             - grid number. 500 points per dimention if not specified
#
# show_progress - 'yes' if progressbar is needed
#
def ultimate(func, xmin = -1., xmax = 1., ymin = -1., ymax = 1., focus = -1, N = 500, show_progress = ''):
    #creating grid with number of points = N
    xs = linspace(xmin, xmax, num = N)[:, newaxis] 
    ys = linspace(ymin, ymax, num = N)
    
    #calculating values on the grid
    gen = abs(func(xs, ys, rg(xs, ys), phig(xs, ys)))
    
    #adjusting the focus if it's not specified
    if focus < 0:
        focus = focusing(gen)
    
    #filtering points where |func - 0| < focus
    points = putpot(gen, xs, ys, focus)
    
    #calculating minimal distance between clusters
    cell = sqrt(((xmax - xmin)/N)**2 + ((ymax - ymin)/N)**2)
    difractor = cell*murmur
    
    #clustering and packing points into lists of lists
    xs, ys = pack(points, difractor, show_progress)
    
    return xs, ys

########################################################################################################################

# auxiliary function for quick plot
#
# xs, ys       - packs of lists of point coordinates. The size of each list in a pair (xs[o], ys[o])
#                must be shared inside the pair, but may be individual for each pair
#
# color        - the color
#
# (xmin, xmax) - x range
# (ymin, ymax) - y range
#
def mplot(xs, ys, color = 'blue', xmin = -1., xmax = 1., ymin = -1., ymax = 1.):
    for o in range(len(xs)):
        plot(xs[o], ys[o], color)
    axis('square')
    xlim(xmin, xmax)
    ylim(ymin, ymax)

########################################################################################################################

# Functions not for external usage

murmur = 5

def rg(x, y):
    return sqrt(x*x + y*y)

def phig(x, y):
    ret = arctan2(y, x)
    return ret

def putpot(gen, xs, ys, eps):
    X = []
    for o in range(xs.size):
        for e in range(ys.size):
            if abs(gen[o, e]) < eps:
                X.append([xs[o], ys[e]])
    return X

def focusing(gen):
    L = gen.size
    trig = int(sqrt(L))
    return 3*sort(gen.copy('C').flatten('C'))[trig]

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