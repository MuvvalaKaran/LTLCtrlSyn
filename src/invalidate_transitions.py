from src.trans_sys_polytope import TransSysToPolytope as trans_sys
from src.read_data import ReadData
import polytope as pc
import numpy as np
import scipy.optimize as opt

# eliminate from Tp transitions that cannot be satisfied due to drift and restrictions on control
# Tp currently has transitions based only on adjacency of states, and loops in every state
# due to system dynamics, some transitions canot be satisfied (we cannot gurantee that from every inital state in a polytope we will reach a neighbour polytope )
# Also, it is possible that not all initial conditions from a polytope can be kept inside, case in which we will eliminate the self-loop
# Transitions will be invalidated if we cannot find control for all the vertices such that some properties be satisfied

# using the combination of both lin and rank produces pretty accurate matrix with few spurious transitions

class Invalid_Transition:
    n = ReadData.D_A.shape[0]
    m = ReadData.U_A.shape[1]
    prec = pow(10,5)*np.finfo(float).eps
    updated_Tp_adj = trans_sys.Tp_adj
    rank_method = True  # this is faster but more restrictive method that eliminates lots of possible transitions
    linprog_method = True  # this method is slightly slower but has more spurious transitions
    # a mix and match also gives a mixed result but seems to be the closest one.

    for i in range(0,len(trans_sys.Tp.get("Tp.Q"))):
        V = trans_sys.Tp.get("Tp.vert")[i]
        H = pc.qhull(V)
        # storing this in its transpose form.  check  which H.b (original is (3,)) you need in all future references
        H.b = np.reshape(H.b, (np.shape(H.A)[0], 1))
        v_no = np.shape(V)[0]
        f_no = np.shape(H.A)[0]
        # f_no = v_no #need to  find  alternative for this jugaad
        F_v = np.matmul(H.A,V.T) - np.tile(H.b,(1,v_no))


        def check(array, val):
            for x in range(np.shape(array)[0]):
                for y in range(np.shape(array)[1]):
                    if array[x][y] <= val:
                        array[x][y] = 1
                    else:
                        array[x][y] = 0
            return array

        def tranfosefor1dvector(array, val):
            #val = 1 for vertical vector n x 1 matrix and 2 for 1 x n matrix
            if (val == 1):
                ret = np.reshape(array,(np.shape(array)[0],1))
            elif(val == 2):
                ret = np.reshape(array,(1,np.shape(array)[0]))
            return ret

        F_v = check(np.abs(F_v),prec)
        centr = np.mean(V,axis=0)
        F_n = np.zeros((f_no,n))
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

        # test f exits to neighbours are feasible (due to control restrictions and drift)
        index_for_neigh = []
        for counter,x in enumerate(updated_Tp_adj[i,:],0):
            if x != 0:
                index_for_neigh.append(counter)

        neigh = set(list(index_for_neigh)).difference({i})
        #  for each neighbour find if transition is possible
        #   first find the common fact of polytope si and sj (which is also the exit facet for si)

        for j in neigh:
            tmp = np.matmul(H.A,np.transpose(np.mean(trans_sys.Tp_vert[j], axis=0)))
            counter = 0
            tmp_T = np.reshape(tmp,(np.shape(tmp)[0],1))
            for x,y in zip(tmp_T,H.b):
                if x > y:
                    pass
                else:
                    break
                counter = counter + 1
            ex_f = counter

        # for all vertices of si check feasibility by checking non-emptiness of optimisation set (imposed by restrictions)
            for l in range(v_no):
                index_for_in_f = []
                for counter, x in enumerate(F_v[:, l], 0):
                    if x != 0:
                        index_for_in_f.append(counter)
                # list_A_for_in_f = index_for_in_f
                in_f = set(list(index_for_in_f)).difference({ex_f})
                in_f = list(in_f)

                if rank_method:
                    H_rep_A = np.vstack((ReadData.U_A, np.matmul(-1*F_n[ex_f, :], ReadData.D_B)))
                    if len(in_f) == 1:
                        H_rep_A = np.vstack((H_rep_A, np.matmul(F_n[in_f[0], :], ReadData.D_B)))
                    else:
                        H_rep_A = np.vstack((H_rep_A, np.matmul(F_n[in_f[0]:in_f[1], :], ReadData.D_B)))

                    abc = np.matmul(ReadData.D_A, tranfosefor1dvector(V[l, :], 1)) + ReadData.D_b
                    H_rep_B = np.vstack((-1 * ReadData.U_b, (np.matmul(F_n[ex_f, :], abc) - prec)))
                    abc = np.matmul(ReadData.D_A, tranfosefor1dvector(V[l, :], 1)) + ReadData.D_b
                    if len(in_f) == 1:
                        H_rep_B = np.vstack((H_rep_B, np.matmul(-1 * F_n[in_f[0], :], abc) - prec))
                    else:
                        H_rep_B = np.vstack((H_rep_B, np.matmul(-1 * F_n[in_f[0]:in_f[1], :], abc) - prec))
                    p = pc.Polytope(H_rep_A, H_rep_B)

                    try:
                        V_rep = pc.extreme(p)
                    except:
                        #if error from v-rep of polytope then disable this transition
                        updated_Tp_adj[i, j] = 0

                    # abc = np.ones((np.shape(V_rep)[0],1))
                    # if(np.linalg.matrix_rank(np.vstack((V_rep, abc)))) != (m+1):
                    # the above two lines a re a better alternative than this
                    if isinstance(V_rep, type(None)):
                        # trans_sys.Tp_adj[i,j] = 0
                        updated_Tp_adj[i, j] = 0
                        break

                if linprog_method:
                    if len(in_f) == 1:
                        abcd1 = np.vstack((np.matmul(-1*F_n[ex_f, :], ReadData.D_B), np.matmul(F_n[in_f[0], :], ReadData.D_B)))
                    else:
                        abcd1 = np.vstack((np.matmul(-1 * F_n[ex_f, :], ReadData.D_B), np.matmul(F_n[in_f[0]:in_f[1], :], ReadData.D_B)))
                    A_check = np.vstack((ReadData.U_A, abcd1))

                    tmp = np.matmul(ReadData.D_A, tranfosefor1dvector(V[l, :], 1)) + ReadData.D_b
                    # tmp1 = np.matmul(-1*F_n[in_f,:],tmp) + ReadData.D_b
                    if len(in_f) == 1:
                        last_stack = np.matmul(-1*F_n[in_f[0], :], tmp) - prec
                    else:
                        last_stack = np.matmul(-1*F_n[in_f[0]:in_f[1], :], tmp) - prec
                    tmp = np.matmul(ReadData.D_A, tranfosefor1dvector(V[l, :], 1)) + ReadData.D_b
                    second_last_stack = np.matmul(F_n[ex_f, :], tmp) - prec
                    abcd2 = np.vstack((second_last_stack, last_stack))
                    B_check = np.vstack((-1*ReadData.U_b, abcd2))
                    sol = opt.linprog(np.matmul(-1*F_n[ex_f, :], ReadData.D_B), A_check, B_check, None, None,
                                      bounds=(None, None))
                    if not sol.__getattr__("success"):
                        updated_Tp_adj[i, j] = 0
                    break

        for m in range(0,v_no):
            in_f = np.nonzero(F_v[:,m])
            if(rank_method):
                if(len(in_f) == 1 ):
                    H_rep_A = np.vstack((ReadData.U_A, np.matmul(F_n[in_f[0], :], ReadData.D_B)))
                    tmp = np.matmul(ReadData.D_A,tranfosefor1dvector(V[m,:],1)) + ReadData.D_b
                    H_rep_B = np.vstack((-1*ReadData.U_b, np.matmul(-1 * F_n[in_f[0], :], tmp)))
                else:
                    H_rep_A = np.vstack((ReadData.U_A, np.matmul(F_n[in_f[0]:in_f[1], :], ReadData.D_B)))
                    tmp = np.matmul(ReadData.D_A, tranfosefor1dvector(V[m, :], 1)) + ReadData.D_b
                    H_rep_B = np.vstack((-1 * ReadData.U_b, np.matmul(-1 * F_n[in_f[0]:in_f[1], :], tmp)))
                p = pc.Polytope(H_rep_A, H_rep_B)
                try:
                    V_rep = pc.extreme(p)

                except:
                    updated_Tp_adj[i, i] = 0

                if isinstance(V_rep,type(None)):
                    # trans_sys.Tp_adj[i,i] = 0
                    updated_Tp_adj[i, i] = 0

            if linprog_method:
                if len(in_f) == 1:
                    tmp = np.matmul(F_n[in_f[0], :], ReadData.D_B)
                else:
                    tmp = np.matmul(F_n[in_f[0]:in_f[1], :], ReadData.D_B)
                A_check = np.vstack((ReadData.U_A, tmp))
                tmp = np.matmul(ReadData.D_A, tranfosefor1dvector(V[m, :], 1)) + ReadData.D_b
                if len(in_f) == 1:
                    B_check = np.vstack((-1*ReadData.U_b, np.matmul(-1*F_n[in_f[0], :], tmp)))
                else:
                    B_check = np.vstack((-1*ReadData.U_b, np.matmul(-1*F_n[in_f[0]:in_f[1], :], tmp)))

                sol = opt.linprog(V[m,:] - centr, A_check, B_check, None, None, bounds=(None, None))
                if not sol.__getattr__("success"):
                    updated_Tp_adj[i, i] = 0
                break
    # print("DOne")
    # print(np.transpose(np.nonzero(updated_Tp_adj)))