'''
find sequence of controls to be applied at vertices of polytopes from run
ctrl will be a 1x2 cell;
element ctrl{1}{i} refers to the i-th state from run{1} (prefix); it is a matrix v x m (v-number of vertices of current
polytope, m-number of controls)
the order of lines (giving controls for each vertex) corresponds to the order from Tp.Vert{run{1}(i)} (vertices of current state)
ctrl{2} refers to the suffix of run, which must be repeated infinitely
this structure for control is because there may exist states with different controls at different times, depending on
their position in run
the non-emptiness of run must be tested before running this function
Speed is a structure as control, containing the resulted speeds (drift+control) at vertices of polytopes from run (Speed{1}{i}(j,:)
is a row vector with speed at vertex j)
structure Speed will be useful in plotting speeds at vertices (2D and 3D cases, function plot_vertex_speeds) and can be
used in simulation (if we want to avoid computing control at each point)'''
import numpy as np
import polytope as pc


def check(array, val):
    for x in range(np.shape(array)[0]):
        for y in range(np.shape(array)[1]):
            if array[x][y] <= val:
                array[x][y] = 1
            else:
                array[x][y] = 0
    return array

def control_sequence(Tp, U_A, U_b, D_A, D_B, D_b, run_Tp):
    ctrl =  []
    ctrl_1= []  # ctrl cell 1
    ctrl_2 = []  # ctrl cell 2
    Speed = []
    Speed_1 = []  # Speed cell 1
    Speed_2 = []  # Speed cell 1
    n = np.shape(D_A)[0]
    prec = pow(10, 5) * np.finfo(float).eps

    compl_run = [run_Tp]
    for i in range(len(compl_run) - 1):
        s_i = compl_run[i]
        s_j = compl_run[i+1]

        V = Tp.get("Tp_vert")[s_i]
        H = pc.qhull(V)
        v_no = np.shape(V)[0]
        f_no = np.shape(H.A)[0]
        F_v = np.matmul(H.A, V.T) - np.tile(H.b, (1, v_no))
        F_v = check(np.abs(F_v), prec)
        centr = np.mean(V, axis=0)
        F_n = np.zeros((f_no, n))

        for k in range(f_no):
            for counter,x in enumerate(list(F_v[k,:]),0):
                if x == 1:
                    index = counter
                    break

            vect = V[index,:] - centr
            vect_transpose = np.reshape(vect,(np.shape(vect)[0],1))
            if(np.shape(np.sign(np.matmul(H.A[k,:], vect_transpose)))[0] == 1):
                tmp =  np.asscalar(np.sign(np.matmul(H.A[k,:], vect_transpose)))
                F_n[k,:] =  (tmp * H.A[k,:])/np.linalg.norm(H.A[k,:])
            else:
                F_n[k, :] = (np.matmul(np.sign(np.matmul(H.A[k,:], vect_transpose)),H.A[k, :])) / np.linalg.norm(H.A[k, :])

        controls = np.zeros(v_no, np.shape(D_B)[1])
        speeds = np.zeros((v_no,n))

        if s_i != s_j :
            # for j in neigh:
            tmp = np.matmul(H.A, np.transpose(np.mean(Tp.get("Tp_vert")[s_j], axis=0)))
            counter = 0
            tmp_T = np.reshape(tmp, (np.shape(tmp)[0], 1))
            for x, y in zip(tmp_T, H.b):
                if x > y:
                    pass
                else:
                    break
                counter = counter + 1
            ex_f = counter

            for k in range(len(v_no)):
                in_f = []
