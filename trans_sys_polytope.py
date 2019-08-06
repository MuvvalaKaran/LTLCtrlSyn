from read_data import ReadData
import numpy as np
import matplotlib.pyplot as plt
import polytope as pc
import os


class TransSysToPolytope:
    start = os.times()[4]
    Ain = []
    Bin = []
    for i in range(len(ReadData.A)-1):
        Ain.append(ReadData.A[i])
    Ain = np.array(Ain)
    for i in range(len(ReadData.B)-1):
        Bin.append(ReadData.B[i])
    Bin = np.array(Bin)
    x,n = Ain.shape
    Nh,y = Bin.shape # numbr of hyperplanes
    sp_no = 0 #subpolytop number
    N_p = len(ReadData.A) - 1
    ind = []
    # Nh = 11
    if Nh > 10:
        n_h = 5
        step_n = 5
        x = min(step_n,(Nh-n_h))
        for i in range(pow(2,Nh)-1):
            ind.append(i)
            # ind = np.array(ind)
        while x > 0:
            new_ind = []
            for i in range(len(ind)):
                for j in range(pow(2,x-1)-1):
                    index = j*pow(2,n_h)+i
# need to work from here on. Also need to understand on whats going on in this code.


    else:
        for i in range(pow(2,Nh)):
            ind.append(i)
    lst = []
    signs = [] #probably should be initialized inside the for loop
    Tp_vert = [] # equivalent of Tp.Vert
    Tp_Signs = [] # equivalent of Tp.signs
    for i in range(pow(2,Nh)):

        a = format(i,'b')
        addZeros = 10 - len(a)
        string_val   = "".join('0' for i in range(addZeros)) #this is our s
        lst.append(string_val + a) # this is equivalent to matlab dec2bin except matlab stores the numbers in matrix

        #format while in our case of python it is being stored as str
        tmplist = []
        for j in range(len(lst[i])):
            sign = pow(-1,int(lst[i][j]))
            tmplist.append(sign)
        signs.append(tmplist)
        H_A = np.matmul(np.diag(signs[i]),Ain)
        H_A = np.append(H_A,ReadData.A[len(ReadData.A)-1],0)
        H_B = np.diag(np.outer(np.array(signs[i]),Bin))
        H_B = np.append(H_B[:,None],ReadData.B[len(ReadData.B)-1],0)
        np.multiply(-1,H_B,H_B)
        # create a vertex representation of sub -polytopes (if such a polytope exists)
        Spol_P = pc.Polytope(H_A,H_B)
        Spol = pc.extreme(Spol_P)
        if(isinstance(Spol,type(None))):
            pass
        else:
            if (Spol.shape[0] > n and np.linalg.matrix_rank(np.hstack((Spol,np.ones((Spol.shape[0],1))))) == n+1):
                sp_no = sp_no + 1
                Tp_vert.append(Spol)
                # a loop only to strip each element in list and add it manually to an array
                tmp_lst_of_ints = [int(x) for x in lst[i]]
                Tp_Signs.append(np.array(tmp_lst_of_ints))

    print("Done with the first loop and now entering the second loop")
    signs = []
    Tp_Q = [i for i in range(sp_no)]
    # TODO if this guy should be initiliazed as empty or zeros_as_empty inserts sporadic numbers
    Tp_adj = np.zeros((sp_no,sp_no))
    Tp_obs = np.zeros((1,sp_no)) #can start from one only as starting form zeros will return null
    for i in range(0,sp_no):
        #find adjacency for polytope i
        signs = Tp_Signs[i]
        Tp_adj[i,i] = 1
        # j~=i; it's possible to have more than one difference of sign between 2
        # adjacent states (see below) - if some props define the same hyperplane
        j = set(list(range(0, sp_no))).difference({i})
        for index in j:
            counter = 0
            inequal = []
            for x,y in zip(signs, Tp_Signs[index]):
                if(x == y):
                    counter = counter + 1
                else:
                    inequal.append(counter) #propositions giving differences between signs of states i and j
                    counter = counter + 1
            tmp_array_for_rank = []
            for row in inequal:
                tmp_array_for_rank.append(np.hstack([[Ain[row,:]],[Bin[row,:]]]))
            tmp_array_for_rank = np.vstack(tmp_array_for_rank)
            if (np.linalg.matrix_rank(tmp_array_for_rank) == 1):
                Tp_adj[i, index] = 1

        # find observable(s) of subpolytope i;observables are indices from alphabet_set (so there is only one observable
        # per state)
        #start with no observable and add observables in a vector (ap_obs will contain numbers (not indices in alphabet) of observed atomic props in current state)
        ap_obs = []
        # for each atomic proposition
        for j in range(0,N_p):
            # all signs corresponding to porp j are 0, so rop j is satisfied by current polytope (i)
            if ReadData.A[j].ndim == 1:
                tmp = signs[0:1]
                if not np.any(tmp):
                    ap_obs.append(j)
                signs = np.delete(signs, np.s_[0:1])
            else:
                tmp = signs[0:ReadData.A[j].shape[0]]
                # check if tmp is all zeroes or not
                if not np.any(tmp):
                    ap_obs.append(j)
                signs = np.delete(signs, np.s_[0:ReadData.A[j].shape[0]])

        def convert(list):
            # Converting integer list to string list
            # and joining the list using join()
            s = [str(i) for i in list]
            res = "".join(s)
            return res

        if np.size(ap_obs) == 0:
            Tp_obs[0][i] = pow(2,N_p)
        else:
            alph_ind = np.zeros((1,N_p),int)
            for alp_index in ap_obs:
                alph_ind[0][alp_index] = 1
            #covert the laph_ind into one string
            tmp = convert(alph_ind.tolist()[0])
            Tp_obs[0][i] = int(tmp,2)
    # created a dictionary of Transition system
    Tp = {
        "Tp.vert":Tp_vert,
        "Tp.Signs":Tp_Signs,
        "Tp.Q":Tp_Q,
        "Tp.adj":Tp_adj,
        "Tp.obs":Tp_obs
    }
    print("---------------------------------------------------------------")
    end = os.times()[4]
    print("class time"  + str(end-start))