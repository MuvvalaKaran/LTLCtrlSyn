from read_data import ReadData
import numpy as np
import matplotlib.pyplot as plt
import sys
import cdd
import polytope as pc
import time

class TransSysToPolytope:
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
        for i in range(pow(2,Nh)-1):
            ind.append(i)
    #print(ind)
    lst = []
    signs = [] #probably should be initialized inside the for loop
    Tp_vert = [] # equivalent of Tp.Vert
    Tp_Signs = [] # equivalent of Tp.signs
    for i in range(pow(2,Nh) -1):

        a = format(i,'b')
        addZeros = 10 - len(a)
        string_val   = "".join('0' for i in range(addZeros)) #this is out s
        lst.append(string_val + a) # this is equivalent to matlab dec2bin except matlab stores the numbers in matrix
        #format while in our case of python it is being stored as str
        tmplist = []
        for j in range(len(lst[i])):
            sign = pow(-1,int(lst[i][j]))
            tmplist.append(sign)
            # print(sign)
        signs.append(tmplist)
        # print("*******************************************************")
        H_A = np.matmul(np.diag(signs[i]),Ain)
        H_A = np.append(H_A,ReadData.A[len(ReadData.A)-1],0)
        # H_B = np.matmul(np.matmul(np.ones(10), signs[i]),Bin)

        # H_B = np.matmul(np.array(signs[i]),Bin)
        # H_B = np.append(H_B,ReadData.B[len(ReadData.B-1)],0)
        # H = np.insert(H,[2,2],0)
        # print(np.dot(np.array(signs[i]),Bin))
        # C = np.array(signs[i]).dot(Bin)
        # for k in range(len(signs[i])):
        #     signs[i][k] = -1*signs[i][k]
        H_B = np.diag(np.outer(np.array(signs[i]),Bin))
        # print(ReadData.B[len(ReadData.B)-1].shape)
        H_B = np.append(H_B[:,None],ReadData.B[len(ReadData.B)-1],0)
        np.multiply(-1,H_B,H_B)
        # create a vertex representation of usb -polytopes (if such a polytope exists)
        Spol_P = pc.Polytope(H_A,H_B)
        Spol = pc.extreme(Spol_P)
        # if(Spol is_instance None):
        if(isinstance(Spol,type(None))):
            pass
        else:
            # print(Spol.shape[0])
            # A = np.array([[2,2],[3,2]])
            #
            # sample = np.hstack((A,np.ones((A.shape[0],1))))
            # print(sample)
            # print(np.array([Spol, np.ones((Spol.shape[0],1))]))
            # print(np.hstack((Spol,np.ones((Spol.shape[0],1)))))
            if (Spol.shape[0] > n and np.linalg.matrix_rank(np.hstack((Spol,np.ones((Spol.shape[0],1))))) == n+1):
                #print("good") #all them are good in our case
                sp_no = sp_no + 1

                # Tp_vert2 = np.empty((1,len(lst[i])))

                Tp_vert.append(Spol)
                # Tp_Signs.append(lst[i])
                # a loop only to strip each element in list and add it manually to an array
                # Tp_Signs.append(list(lst[i]))
                tmp_lst_of_ints = [int(x) for x in lst[i]]
                Tp_Signs.append(np.array(tmp_lst_of_ints))
                # for element in range(len(lst[i])):
                #     # print(element)
                # # print("***************************************\n")
                #     lst_to_array = np.empty((1,len(lst[i])))
                #     # lst_to_array[1,element] = lst[i]
                #     np.insert(lst_to_array,element,int(lst[i][element]))
                # Tp_Signs.append(lst_to_array)


                # tmp = pc.qhull(Spol)
                # tmp.plot()
                # plt.show()
                # print("yay")

    # print(Tp_Signs[0].shape)
    print("Done with the first loop and now entering the second loop")

    Tp_Q = [i for i in range(sp_no)] #sp_no should have been 34
    # TODO if this guy should be initiliazed as empty or zeros as empty inserts sporadic numbers
    Tp_adj = np.zeros((sp_no,sp_no))
    Tp_obs = np.zeros((1,sp_no))
    # print(set(Tp_obs_as_list))
    for i in range(sp_no):
        #find adjacency for polytope i
        signs = Tp_Signs[i]
        Tp_adj[i][i] = 1
        # print(signs)

        # j~=i; it's possible to have more than one difference of sign between 2
        # adjacent states (see below) - if some props define the same hyperplane
        # print(set(list(range(1, sp_no))))
        # print({i})
        j =  set(list(range(1, sp_no))).difference({i+1})
        # print(j)
        for index in j:
            # print(index)
            # print(Tp_Signs[index])
            # [[x[0],x[1],y[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9]] for x in Tp_Signs[index] for y in signs if x[0] == y[0]]
            counter = 1
            for x,y in zip(signs, Tp_Signs[index]):
                # print(xy)

                # print(x,y)
                if(x == y):
                    counter = counter + 1
                    # pass
                else:
                    inequal = counter #propositions giving differences between signs of states i and j
                    # print(inequal)
                    break
        if (np.linalg.matrix_rank(np.array([Ain[inequal,:],Bin[inequal,:]])) == 1):
            # print("good")
            Tp_adj[i,index]  = 1
        # print(Tp_adj)
        # print("************************************************************")

        # find observable(s) of subpolytope i;observables are indices from alphabet_set (so there is only one observable
        # per state)
        #start with no observable and add observables in a vector (ap_obs will contain numbers (not indices in alphabet) of observed atomic props in current state)
        ap_obs = []
        # for each atomic proposition
        for j in range(1,N_p):
            # print(ReadData.A[j].shape[0])
            # all signs corresponding to porp j are 0, so rop j is satisfied by current polytope (i)
            # signs[0:ReadData.A[j].shape[0]]
            if ReadData.A[j].ndim == 1:
                tmp = signs[0:1]
            else:
                tmp = signs[0:ReadData.A[j].shape[0]]
        print(tmp)
            # check if tmp is all zeroes or not
        #     if not np.any(tmp):
        #         ap_obs.append(j)
        #     print(ap_obs)
        print("##############################")
        # print(signs[0:ReadData.A[j].shape[0]])


        # condition = indices(signs, lambda Tp_signs: >2)
        # inequal = np.extract(condition=,arr=

        # [[x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9]]for x in signs for y in Tp_Signs[j,:] if x[0] != y[0]]

        def indices(a, func):
            return [i for (i, val) in enumerate(a) if func(val)]








        # print(H_B.shape)
        # abc = []
        # abc.append(H_A)
        # abc.append(H_B)
    # print(abc)

    # p1 = pc.box2poly([[0,2],[0,2]])
    # p2 = pc.box2poly([[2,3],[0,2]])
    # r = pc.Region([p1,p2])
    # for polytope in r:
    #     print(polytope)
    # print(r)
    # p1.plot()
    # if len(sys.argv) < 2:
    #     N = 3
    # else:
    #     N = int(sys.argv[1])
    #
    # V = np.random.rand(N, 2)
    #
    # print("Sampled " + str(N) + " points:")
    # print(V)
    #
    # P = pc.qhull(V)
    # print("Computed the convex hull:")
    # print(P)
    #
    # V_min = pc.extreme(P)
    # print("which has extreme points:")
    # print(V_min)
    #
    # P.plot()
    # plt.show()

    # r.plot()




    # for i in range(10):
    #     b = bin(i)
    #     print(b)


