'''function that simulates the continuous system, by computing the control in each point from continuous trajectory, computing resulted speed and integrating with a time_step
the start point is x0, and should be inside the polytope corresponding to the first state from run (we will start from centroid of this polytope)
the polytope in which we are is triangularized, we find the triangle containing the current position x and we find the control,
having the controls at simplex vertices already computed (in structure ctrl); when the polytope is left, the next one from run will be hit, and we will do the same thing
the function returns three matrices
X is a matrix t_fin x n, giving the position at each time instant (n is the space dimension)
C is a matrix t_fin x m, giving the control applied at each time (m is the number of input controls)
S is the speed (matrix t_fin x n), giving the actual speeds
vector t_ev is a vector with number of time_steps when an "event" happened: the prefix is finished or an iteration of suffix is finished
(if final state has a self-loop, t_ev has only one element (when prefix was finished)) t_fin used above is the last element of t_ev
the simulation will be done by following the prefix of run and rep_suf-times its suffix
if final state is a stay-inside state (only one state in run{2}), simulation is stopped when a small distance (prec) is covered in a time_step  '''
import numpy as np
import polytope as pc
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

Debug = False

def simulatesystem(Tp, D_A, D_B, D_b, x0, run_Tp, ctrl, time_step, rep_suf):
    prec = pow(10, 5) * np.finfo(float).eps
    n = np.shape(D_A)[0]
    t_s = 0
    stop = 0
    t_ev = []

    # run_Tp = [int(item) for cell in run_Tp for subcell in cell for item in subcell]

    compl_run = [int(item) for cell in run_Tp for subcell in cell for item in subcell]
    # compl_ctrl = [array for sublist in ctrl for array in sublist]
    compl_ctrl = []

    for sublist in ctrl:
        for array in sublist:
            compl_ctrl.append(array)
    if len(run_Tp[0][1]) != 1:
        for i in range(rep_suf - 1):
            # compl_run.append([i  for i in run_Tp[0][1]])
            # compl_ctrl.append([array for array in ctrl[0][1]])
            compl_run = compl_run + [int(item) for item in run_Tp[0][1]]
            # compl_ctrl = compl_ctrl + ctrl[0][1]
            for counter,sublist in enumerate(ctrl):
                for array in sublist:
                    if counter == 1:
                        compl_ctrl.append(array)

    x0 = np.asarray(x0)
    x0 = x0.transpose()
    X = [x0]
    C = []
    S = []
    for i in range(len(compl_run)):
        Vert = Tp.get("Tp.vert")[compl_run[i]]
        Ctr = compl_ctrl[i]
        tes = Delaunay(Vert)

        if Debug:
            for simplices in tes.simplices:

                plt.triplot(tes.points[simplices, 0], tes.points[simplices, 1])
            plt.plot(Vert[:, 0], Vert[:, 1], 'o')
            plt.pause(0.1)
            plt.show()

        # find = tes.vertex_to_simplex(tes.find_simplex(x0.transpose()))
        xfortes = X[-1].transpose()
        isinsidepoly = tes.find_simplex(np.transpose(xfortes))  # i believe this is probably right

        # simpl = tes.vertex_to_simplex()
        # print("Testing testing")
        while isinsidepoly != -1 and stop is not True:
            t_s = t_s + 1
            x = X[-1]
            x = x.transpose()
            new_Ctr = np.ndarray((3,2))
            for_inv = np.ndarray((3,2))
            for i in range(np.shape(tes.vertices)[1]):
                new_Ctr[i, :] = Ctr[tes.vertices[isinsidepoly, i], :]
                for_inv[i, :] = Vert[tes.vertices[isinsidepoly, i], :]

            stackedtomakesquarematrix = np.vstack((for_inv.transpose(), np.ones((1, n+1))))
            inverseofabovematix = np.linalg.inv(stackedtomakesquarematrix)

            tmp = np.matmul(new_Ctr.transpose(), inverseofabovematix)
            getxmatrixtoshape = np.vstack((x, [1]))
            u_x = np.matmul(tmp, getxmatrixtoshape)
            speed = np.matmul(D_A,x) + np.matmul(D_B,u_x) + D_b

            new_x = x + (speed*time_step)
            X.append(new_x.transpose())
            C.append(u_x.transpose())
            S.append(speed.transpose())

            isinsidepoly = tes.find_simplex(X[-1])
            if Debug:
                if isinsidepoly == -1:
                    print("Changing Polytope at time step :", t_s)
            if i == len(run_Tp[0][0]) and np.linalg.norm(new_x - x) <= prec:
                stop = True

        if i >= len(run_Tp[0][0]) and np.mod((i - len(run_Tp[0][0])), len(run_Tp[0][1])) == 0:
            t_ev.append(t_s)

    if t_ev[-1] != t_s:
        t_ev.append(t_s)

    X.append([])

    return t_ev, X, C, S


