import polytope as pc
import numpy as np
import matplotlib.patches
import matplotlib.pyplot as plt
import sys
import os
import imageio
import shutil
from itertools import cycle


class PlotTransitionSystem(object):

    def __init__(self, Tp, A, b):
        self.Tp = Tp
        self.A = A
        self.b = b

    def _get_patch(self, poly1, **kwargs):
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

    def ismember(self, a, b):
        ret = False
        for counter, i in enumerate(b):

            if a == i:
                ret = True
                break
        return ret

    def make_gif(self, input_folder, save_filepath):
        episode_frames = []
        time_per_step = 0.2
        for root, _, files in os.walk(input_folder):
            file_paths = [os.path.join(root, file) for file in files]

            # sorted by modified time
            file_paths = sorted(file_paths, key=lambda x: os.path.getmtime(x))
            episode_frames = [imageio.imread(file_path)
                              for file_path in file_paths if file_path.endswith('.png')]
        episode_frames = np.array(episode_frames)
        imageio.mimsave(save_filepath, episode_frames, duration=time_per_step)

    def PlotTraSys(self, nargmin, accepted_Q0):
        """
        Plot sub polytopes of the transition sysytem.
        :param nargmin:
        :param accepted_Q0:
        :return:
        """

        # create two different names for initial TS and for TS with valid set of initial states for a given
        # specification
        if nargmin:
            # clear the previous frame
            shutil.rmtree('./frames/')
            os.makedirs('frames')
            plot_name = 'ts_init'
        else:
            plot_name = 'ts'

        Tp = self.Tp
        A = self.A[-1]
        b = self.b[-1]

        Tp_Q = Tp.get("Tp.Q")
        Tp_vert = Tp.get("Tp.vert")
        updated_Tp_adj = Tp.get("Tp.adj")

        print("Plotting transition system on polytopes")
        nargmin = nargmin

        if nargmin:
            # accepted_Q = initStates.getAccept_Q0()
            accepted_Q0 = accepted_Q0

        if np.shape(A)[0] == np.shape(b)[0]:
            pass
        else:
            print("Ensure the number of row of A and b matrix corresponding to the state space boundaries are same")

        p = pc.Polytope(A, b)
        bound = pc.extreme(p)

        if isinstance(bound, type(None)):
            p = pc.Polytope(A, -1*b)
            bound = pc.extreme(p)
            print("Tried with reversing the signs of b matrix")

        if isinstance(bound, type(None)):
            print("PLease make sure the state space boundaries form a convex polytope")
            sys.exit(1)

        n = np.shape(A)[1]  # space dimension

        if n == 2:
            ep = (np.amax(bound, axis=0) - np.amin(bound, axis=0))/20

            xmin = np.amin(bound[:, 0]) - ep[0]
            xmax = np.amax(bound[:, 0]) + ep[0]
            ymin = np.amin(bound[:, 1]) - ep[1]
            ymax = np.amax(bound[:, 1]) + ep[1]

            fig = plt.figure()
            time_step = 0

            ax = fig.add_subplot(111)
            ax.add_patch(self._get_patch(p,
                                         edgecolor="Black",
                                         linewidth=0.5,
                                         facecolor=None,
                                         fill=False))
            plt.pause(0.1)
            plt.savefig(f"frames/{plot_name+str(time_step)}.png", dpi=200)

            centr = np.zeros((len(Tp_Q), n))
            for i in range(len(Tp_Q)):
                time_step += 1
                k = pc.qhull(Tp_vert[i])

                tmp = self._get_patch(k,
                                      edgecolor="Black",
                                      linewidth=0.15,
                                      facecolor=None,
                                      fill=False)
                ax.add_patch(tmp)
                plt.xlim(xmin, xmax)
                plt.ylim(ymin, ymax)

                plt.pause(0.1)
                plt.savefig(f"frames/grid_{time_step}.png", dpi=200)

                centr[i, :] = np.mean(Tp_vert[i], axis=0)  # taking mean along the columns

                if nargmin:
                    if self.ismember(i, accepted_Q0):
                        k = pc.qhull(Tp_vert[i])
                        tmp = self._get_patch(k,
                                              edgecolor="Black",
                                              linewidth=0.15,
                                              facecolor="Green",
                                              fill=True)
                        ax.add_patch(tmp)
                    else:
                        k = pc.qhull(Tp_vert[i])
                        tmp = self._get_patch(k,
                                              edgecolor="Black",
                                              linewidth=0.15,
                                              facecolor="Blue",
                                              fill=True)
                        ax.add_patch(tmp)

            if not nargmin:
                for i in range(len(Tp_Q)):
                    time_step += 1
                    j = [0 for k in range(len(Tp_Q))]
                    neigh = []
                    tmp_neigh = np.nonzero(updated_Tp_adj[i, :])
                    neig_w_smaller_index = np.where((tmp_neigh[0] < i))
                    neig_w_smaller_index = [int(x) for x in neig_w_smaller_index[0]]
                    for element in neig_w_smaller_index:
                        neigh.append(tmp_neigh[0][element])

                    neigh_w_larger_index = np.where(tmp_neigh[0] > i)
                    neigh_w_larger_index = [int(x) for x in neigh_w_larger_index[0]]
                    for element in neigh_w_larger_index:
                        neigh.append(tmp_neigh[0][element])

                    for index in neig_w_smaller_index:
                        j[index] = 1

                    for index in neigh_w_larger_index:
                        j[index] = 1

                    for counter, index_of_j in enumerate(j):
                        if counter < i:
                            if updated_Tp_adj[i, counter] != 0:
                                plt.plot([centr[i, 0], centr[counter, 0]],
                                         [centr[i, 1], centr[counter, 1]],
                                         linestyle='--',
                                         color='r')
                                plt.plot(centr[i, 0],
                                         centr[counter, 0],
                                         centr[i, 0],
                                         centr[i, 1],
                                         'ro')
                                plt.pause(0.1)

                            # else:
                                # plt.plot(centr[i, 0], centr[i, 1], centr[counter, 0], centr[counter, 1], 'g.')
                                # plt.pause(0.1)

                        elif counter > i:
                            if updated_Tp_adj[i, counter] != 0:
                                plt.plot([centr[i, 0], centr[counter, 0]],
                                         [centr[i, 1], centr[counter, 1]],
                                         linestyle='-',
                                         color='r')

                                plt.plot(centr[i, 0],
                                         centr[counter, 0],
                                         centr[i, 0],
                                         centr[i, 1],
                                         'ro')
                                plt.pause(0.1)
                            # else:
                            #     plt.plot(centr[i, 0], centr[i, 1], centr[counter, 0], centr[counter, 1], 'g.')
                            #     plt.pause(0.1)

                    if updated_Tp_adj[i, i] != 0:
                        plt.plot(centr[i, 0], centr[i, 1], 'r*')
                        plt.pause(0.1)

                    plt.savefig(f"frames/{plot_name+str(time_step)}.png", dpi=200)

            for i in range(len(Tp_Q)):
                plt.text(centr[i, 0], centr[i, 1], "q_" + str(i), fontsize=8, horizontalalignment='center',
                         verticalalignment='center')

            time_step += 1
            plt.savefig(f"frames/{plot_name + str(time_step)}.png", dpi=200)

        elif n == 3:
            pass
        else:
            print("Cannot display more than 3 dimension transition system")

        # only make a gif when we plotting the set of valid initial states
        if nargmin:
            self.make_gif('./frames/', f'./gifs/ts_init.gif')

        return ax