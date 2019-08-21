''' represent a run of transition system on polytopes (if found)
run is represented by coloring the polytopes ()
this run satisfies LTL formula '''
import numpy as np
import polytope as pc
import matplotlib.pyplot as plt

def _get_patch(poly1, **kwargs):
    """Return matplotlib patch for given Polytope.

    Example::

    > # Plot Polytope objects poly1 and poly2 in the same plot
    > import matplotlib.pyplot as plt
    > fig = plt.figure()
    > ax = fig.add_subplot(111)
    > p1 = _get_patch(poly1, color="blue")
    > p2 = _get_patch(poly2, color="yellow")
    > ax.add_patch(p1)
    > ax.add_patch(p2)
    > ax.set_xlim(xl, xu) # Optional: set axis max/min
    > ax.set_ylim(yl, yu)
    > plt.show()

    @type poly1: L{Polytope}
    @param kwargs: any keyword arguments valid for
        matplotlib.patches.Polygon
    """
    import matplotlib as mpl
    V = pc.extreme(poly1)
    rc, xc = pc.cheby_ball(poly1)
    x = V[:, 1] - xc[1]
    y = V[:, 0] - xc[0]
    mult = np.sqrt(x**2 + y**2)
    x = x / mult
    angle = np.arccos(x)
    corr = np.ones(y.size) - 2 * (y < 0)
    angle = angle * corr
    ind = np.argsort(angle)
    # create patch
    patch = mpl.patches.Polygon(V[ind, :], True, **kwargs)
    patch.set_zorder(0)
    return patch

class PlotRun():

    def __init__(self, Tp, run_Tp, h_fig):
        self.Tp = Tp
        self.run_Tp = run_Tp
        self.h_fig = h_fig

    def plotrun(self):

        Tp = self.Tp
        run_Tp = self.run_Tp
        n = np.shape(Tp.get("Tp.vert")[0])[1]
        ax = self.h_fig
        Tp_vert = Tp.get("Tp.vert")
        # fig = plt.figure()
        # ax = fig.add_subplot(111)

        if len(run_Tp) == 0:
            print("LTL formula cannot be satisfied")
            return

        if n == 2:
            states = run_Tp[0][0]
            for i in states:
                k = pc.qhull(Tp_vert[int(i)])
                tmp = _get_patch(k, edgecolor="Black", linewidth=0.15, facecolor="gray", fill=True)
                ax.add_patch(tmp)
                # plt.pause(0.1)
                plt.pause(0.1)

            states = run_Tp[0][0][-1] + run_Tp[0][1]
            states = [int(i) for i in states]

            for i in states[:-1]:
                k = pc.qhull(Tp_vert[i])
                tmp = _get_patch(k, edgecolor="Black", linewidth=0.15, facecolor="pink", fill=True)
                ax.add_patch(tmp)
                plt.pause(0.1)
                # ax.show()

