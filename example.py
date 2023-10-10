import matplotlib.pyplot as plt
import numpy as np
import ligraph2 as lg

#The example of usage

def examplefunc2(x, y, r, phi):
        return (np.log(np.abs(phi - 0.1*(3-y)*np.cos(30*phi))))**(x - 0.6*y) + np.sin(r) - 1
    
def examplefunc1(x, y, r, phi):
    return x + y - r - phi

def examplefunc(x, y, r, phi):
    return np.sin(x + phi) + np.log(r + x) - 1/y - 1

def example():
    #defining constants
    
    x0 = -9
    x1 = 9
    y0 = -9
    y1 = 9
    focus = 0.05 #adjust focus for more or less THICC graph
    N = 500 #adjust this parameter to make the grid more or less detailed

    #calculate graphs
    #xs and ys contain some number of corresponding lists of points. Each pair of these lists draws one part of a total graph
    xs, ys = lg.ultimate(examplefunc, xmin = x0, xmax = x1, ymin = y0, ymax = y1)
    
    #plot graphs with red color
    lg.mplot(xs, ys, color = 'red', xmin = x0, xmax = x1, ymin = y0, ymax = y1)
    plt.show()
    
example()