import numpy as np
from numba import jit

if __package__ is None or __package__ == '':
    from fractal_result import fractal_result
else:
    from .fractal_result import fractal_result


@jit
def _lyapunov(string, xbound, ybound, n_init=100, n_iter=100, width=3, height=3, dpi=100):

    """
        returns a Lyupanov fractal according to the proved string (e.g. 'ABAA')
    """

    xmin, xmax = [float(xbound[0]), float(xbound[1])]
    ymin, ymax = [float(ybound[0]), float(ybound[1])]
    
    nx = width*dpi
    ny = height*dpi

    xvals = np.array([xmin + i*(xmax - xmin)/nx for i in range(nx)], dtype=np.float64)
    yvals = np.array([ymin + i*(ymax - ymin)/ny for i in range(ny)], dtype=np.float64)

    length = len(string)
    lattice = np.zeros((int(nx), int(ny)), dtype=np.float64)

    for i in range(len(xvals)):
        for j in range(len(yvals)):

            xv = xvals[i]
            yv = yvals[j]
            selector = {'A': xv, 'B': yv}
            n = 0

            x = 0.5
            for _init in range(n_init):
            
                str_val = string[n % length]
                rn = selector[str_val]
                n += 1
            
                x = (rn*x)*(1-x)

            lamd = 0.0
            for _iter in range(n_iter):

                str_val = string[n % length]
                rn = selector[str_val]
                n += 1

                x = (rn*x)*(1-x)
                lamd += np.log(np.abs(rn-2*rn*x))
            
            lattice[i, j] += lamd/n_iter

    return (lattice.T, width, height, dpi)


def lyapunov(string, xbound, ybound, n_init=100, n_iter=100, width=3, height=3, dpi=100):

    res = _lyapunov(string, xbound, ybound, n_init=n_init, n_iter=n_iter,
                    width=width, height=height, dpi=dpi)

    return fractal_result(*res)
