from trans_sys_polytope import TransSysToPolytope as trans_sys
from read_data import ReadData
import polytope as pc
import numpy as np

# eliminate from Tp tansitions that cannot be saisfied due to drift and restrictions on control
# Tp currently has transitions based only on adjacency of states, and loops in every state
# due to system dynamics, come transitions canot be satisfied (we cannot gurantee that from every inital state in a polytope we will reach a neighbour polytope )
# Also, it is possible that not all initial conditions from a polytope can be kept inside, case in which we will eliminate the self-loop
# Transitions will be invalidate if we cannot find control for all the vertices such that some properties be satisfied

n = ReadData.D_A.shape[0]
m = ReadData.U_A.shape[1]
prec = pow(10,5)*np.finfo(float).eps
print(prec)
# print(n,m)
for i in range(len(trans_sys.Tp.get("Tp.Q"))):
    V = trans_sys.Tp.get("Tp.vert")[i]
    H = pc.qhull(V)
    # storing this in its transpose form.  check  which H.b (original is (3,)) you need in all future references
    H.b = np.reshape(H.b, (3, 1))
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

    F_v = check(np.abs(F_v),prec)
    centr = np.mean(V,axis=0)
    F_n = np.zeros((f_no,n))
    for i in range(f_no):
        pass

    # print(F_v)



    # print(np.shape(H.b))
    # print(np.ndim(H.b))
    # print(np.matmul(H.A,V.T))
    # print(np.transpose(H.b).shape)
    # print(np.tile(H.b,(1,3)))
    # print(np.tile(np.transpose(H.b),3))
    # print(trans_sys.H_A)
    # print(H.dim)


