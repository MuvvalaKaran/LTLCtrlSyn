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
# print(n,m)
for i in range(len(trans_sys.Tp.get("Tp.Q"))):
    V = trans_sys.Tp.get("Tp.vert")[i]
    H = pc.qhull(V)

    v_no = np.shape(V)[0]
    f_no = v_no #need to  find  alternative for this jugaad
    # F_v = np.matmul(H.A,V.T) - np.tile(H.b,(1,v_no))
    print(np.matmul(H.A,V.T))
    print(np.tile(H.b,(3,1)))
    # print(trans_sys.H_A)
    # print(H.dim)