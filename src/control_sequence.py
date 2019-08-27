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
import scipy.optimize as opt


def check(array, val):
    for x in range(np.shape(array)[0]):
        for y in range(np.shape(array)[1]):
            if array[x][y] <= val:
                array[x][y] = 1
            else:
                array[x][y] = 0
    return array


def tranfosefor1dvector(array, val):
    # val = 1 for vertical vector n x 1 matrix and 2 for 1 x n matrix
    if (val == 1):
        ret = np.reshape(array, (np.shape(array)[0], 1))
    elif (val == 2):
        ret = np.reshape(array, (1, np.shape(array)[0]))
    return ret


def control_sequence(Tp, U_A, U_b, D_A, D_B, D_b, run_Tp):
    # ctrl =  []
    ctrl_1= []  # ctrl cell 1
    ctrl_2 = []  # ctrl cell 2
    # Speed = []
    Speed_1 = []  # Speed cell 1
    Speed_2 = []  # Speed cell 1
    n = np.shape(D_A)[0]
    prec = pow(10, 5) * np.finfo(float).eps
    compl_run = [int(item) for cell in run_Tp for subcell in cell for item in subcell]  # merge subcell of cell prefix+suffix of that cell

    for i in range(len(compl_run) - 1):
        s_i = compl_run[i]
        s_j = compl_run[i+1]

        V = Tp.get("Tp.vert")[s_i]
        H = pc.qhull(V)
        v_no = np.shape(V)[0]
        f_no = np.shape(H.A)[0]
        F_v = np.matmul(H.A, V.T) - np.tile(tranfosefor1dvector(H.b, 1), (1, v_no))
        F_v = check(np.abs(F_v), prec)
        centr = np.mean(V, axis=0)
        F_n = np.zeros((f_no, n))

        for k in range(f_no):
            for counter,x in enumerate(list(F_v[k, :]), 0):
                if x == 1:
                    index = counter
                    break

            vect = V[index, :] - centr
            vect_transpose = np.reshape(vect,(np.shape(vect)[0], 1))
            if np.shape(np.sign(np.matmul(H.A[k, :], vect_transpose)))[0] == 1:
                tmp = np.asscalar(np.sign(np.matmul(H.A[k, :], vect_transpose)))
                F_n[k, :] = (tmp * H.A[k, :])/np.linalg.norm(H.A[k, :])
            else:
                F_n[k, :] = (np.matmul(np.sign(np.matmul(H.A[k, :], vect_transpose)), H.A[k, :])) / np.linalg.norm(H.A[k, :])

        controls = np.zeros((v_no, np.shape(D_B)[1]))
        speeds = np.zeros((v_no, n))

        if s_i != s_j:
            # for j in neigh:
            tmp = np.matmul(H.A, np.transpose(np.mean(Tp.get("Tp.vert")[s_j], axis=0)))
            counter = 0
            tmp_T = np.reshape(tmp, (np.shape(tmp)[0], 1))
            for x, y in zip(tmp, H.b):
                if x > y:
                    break
                counter = counter + 1
            ex_f = counter

            for l in range(v_no):
                index_for_in_f = []
                for counter, x in enumerate(F_v[:, l], 0):
                    if x != 0:
                        index_for_in_f.append(counter)
                # list_A_for_in_f = index_for_in_f
                in_f = set(list(index_for_in_f)).difference({ex_f})
                in_f = list(in_f)
                A_Check = np.vstack((U_A, np.matmul(-1 * F_n[ex_f, :], D_B)))
                if (len(in_f) == 1):
                    A_Check = np.vstack((A_Check, np.matmul(F_n[in_f[0], :], D_B)))
                else:
                    A_Check = np.vstack((A_Check, np.matmul(F_n[in_f[0]:in_f[1], :], D_B)))
                abc = np.matmul(D_A, tranfosefor1dvector(V[l, :], 1)) + D_b
                B_Check = np.vstack((-1 * U_b, (np.matmul(F_n[ex_f, :], abc) - prec)))
                abc = np.matmul(D_A, tranfosefor1dvector(V[l, :], 1)) + D_b
                if len(in_f) == 1:
                    B_Check = np.vstack((B_Check, np.matmul(-1 * F_n[in_f[0], :], abc) - prec))
                else:
                    B_Check = np.vstack((B_Check, np.matmul(-1 * F_n[in_f[0]:in_f[1], :], abc) - prec))

                sol = opt.linprog(np.matmul(-1 * F_n[ex_f, :], D_B), A_Check, B_Check, None, None,
                                  bounds=(None, None))

                x = sol.__getitem__('x')  # current solution vector
                fun = sol.__getitem__('fun')  # current value of the object function
                success = sol.__getitem__('success')  # flag for optimization success or failure
                controls[l, :] = tranfosefor1dvector(x, 2)
                # speeds[l, :] = np.transpose(np.matmul(D_A, np.transpose(V[l, :]))
                #                             + np.matmul(D_B, tranfosefor1dvector(x, 1)) + D_b)
                speeds[l, :] = np.matmul(D_A, np.transpose(V[l, :])) + np.ravel(
                    np.matmul(D_B, tranfosefor1dvector(x, 1))) + np.ravel(D_b)

                if (sol.__getattr__("success") == False):
                    print("Bad Optimization for transition between states " + str(s_i) + " and ", str(s_j) + ".")
        else:
            for l in range(v_no):
                # index_for_in_f = []
                in_f = []
                for counter, x in enumerate(F_v[:, l], 0):
                    if x != 0:
                        in_f.append(counter)
                        # index_for_in_f.append(counter)
                # list_A_for_in_f = index_for_in_f
                # in_f = set(list(index_for_in_f)).difference({ex_f})
                # in_f = list(index_for_in_f)



                # A_Check = np.vstack((U_A, np.matmul(-1 * F_n[ex_f, :], D_B)))
                # if (len(in_f) == 1):
                #     A_Check = np.vstack((A_Check, np.matmul(F_n[in_f[0], :], D_B)))
                # else:
                #     A_Check = np.vstack((A_Check, np.matmul(F_n[in_f[0]:in_f[1], :], D_B)))
                # abc = np.matmul(D_A, tranfosefor1dvector(V[l, :], 1)) + D_b
                # B_Check = np.vstack((-1 * U_b, (np.matmul(F_n[ex_f, :], abc) - prec)))
                # abc = np.matmul(D_A, tranfosefor1dvector(V[l, :], 1)) + D_b
                # if len(in_f) == 1:
                #     B_Check = np.vstack((B_Check, np.matmul(-1 * F_n[in_f[0], :], abc) - prec))
                # else:
                #     B_Check = np.vstack((B_Check, np.matmul(-1 * F_n[in_f[0]:in_f[1], :], abc) - prec))

                if (len(in_f) == 1):
                    tmp = np.matmul(F_n[in_f[0], :], D_B)
                else:
                    tmp = np.matmul(F_n[in_f[0]:in_f[1], :], D_B)
                A_Check = np.vstack((U_A, tmp))

                tmp = np.matmul(D_A, tranfosefor1dvector(V[l, :], 1)) + D_b
                if len(in_f) == 1:
                    B_Check = np.vstack((-1 * U_b, np.matmul(-1 * F_n[in_f[0], :], tmp)))
                else:
                    B_Check = np.vstack((-1 * U_b, np.matmul(-1 * F_n[in_f[0]:in_f[1], :], tmp)))

                sol = opt.linprog(V[l, :] - centr, A_Check, B_Check, None, None, bounds=(None, None))

                x = sol.__getitem__('x')  # current colution vector
                fun = sol.__getitem__('fun')  # current value of the object function
                success = sol.__getitem__('success')  # flag for optimization success or failure
                controls[l, :] = tranfosefor1dvector(x, 2)
                # tmp1 = tranfosefor1dvector(np.matmul(D_A, np.transpose(V[l, :])), 1)
                # tmp2 = np.ravel(np.matmul(D_B, tranfosefor1dvector(x, 1)))
                # tmp3 = np.ravel(D_b)
                # tmp4 = tmp1 + tmp2 + tmp3
                speeds[l, :] = np.matmul(D_A, np.transpose(V[l, :])) + np.ravel( np.matmul(D_B, tranfosefor1dvector(x, 1))) + np.ravel(D_b)
                # speeds[l, :] = tmp1 + tmp2 + tmp3

                if not sol.__getattr__("success"):
                    print("Bad Optimization for self-loop in state " + str(s_i))

        if i < len(run_Tp[0][0]):
            ctrl_1.append(controls)
            Speed_1.append(speeds)
        else:
            ctrl_2.append(controls)
            Speed_2.append(speeds)

    ctrl_2.append(ctrl_1[-1])  # insert at the last element
    Speed_2.append(Speed_1[-1])  # insert at the last element

    ctrl = [ctrl_1] + [ctrl_2]
    Speed = [Speed_1] + [Speed_2]

    return ctrl, Speed





