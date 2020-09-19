import numpy as np
import polytope as pc
import imageio
import os
import matplotlib.pyplot as plt


class PlotDrift:
    """
    A class that plots the drift induces by the dynamics of the system within the space boundaries

    THe affine drift: dot(x) = D_Ax + D_B
    """
    def __init__(self, init_fig, D_A, D_b, A_bound, B_bound):
        self.init_fig = init_fig
        self.D_A = D_A
        self.D_b = D_b
        self.A_bound = A_bound
        self.b_bound = B_bound

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

    def plotdrift(self):

        A = self.A_bound
        b = self.b_bound
        D_A = self.D_A
        D_b = self.D_b
        ax = self.init_fig

        Bound = pc.Polytope(A, -1*b)
        Bound_V = pc.extreme(Bound)
        n = np.shape(A)[1]
        # ax = trans_plot.plt
        p_no = 0.4
        x_start = np.amin(Bound_V[:, 0], axis=0)
        x_stop = np.amax(Bound_V[:, 0], axis=0)
        y_start = np.amin(Bound_V[:, 1], axis=0)
        y_stop = np.amax(Bound_V[:, 1], axis=0)
        lin_x = np.arange(x_start, x_stop, p_no)
        lin_y = np.arange(y_start, y_stop, p_no)

        if n == 2:
            X, Y = np.meshgrid(lin_x, lin_y)
            Gx = D_A[0, 0]*X + D_A[0, 1]*Y + D_b[0, 0]
            Gy = D_A[1, 0]*X + D_A[1, 1]*Y + D_b[1, 0]
            ax.quiver(X, Y, Gx, Gy)
            # ax.xaxis.set_ticks([])
            # ax.yaxis.set_ticks([])
            # ax.show()
            plt.pause(0.01)

        if n ==3:
            z_start = np.amin(Bound_V[:, 2], axis=0)
            z_stop = np.amax(Bound_V[:, 2], axis=0)
            lin_z = np.array(z_start, z_stop, p_no)
            X, Y, Z = np.meshgrid(lin_x, lin_y, lin_z)
            Gx = D_A[0, 0] * X + D_A[0, 1] * Y + D_b[0, 0]
            Gy = D_A[1, 0] * X + D_A[1, 1] * Y + D_b[1, 0]
            Gz = D_A[2, 0] * X + D_A[2, 1] * Y + D_b[2, 0]
            ax.quiver(X, Y, Z, Gx, Gy, Gz)
            # ax.show()
            plt.pause(0.01)

        plt.savefig(f"frames/grid_{1000}.png", dpi=200)
        self.make_gif('./frames/', f'./gifs/ts.gif')

        return ax

