from read_data import ReadData
import numpy as np
import cdd

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
    Nh,y = Bin.shape
    sp_no = 0
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
    for i in range(pow(2,Nh) -1):

        a = format(i,'b')
        addZeros = 10 - len(a)
        string_val   = "".join('0' for i in range(addZeros))
        lst.append(string_val + a) # this is equivalent to matlab dec2bin except matlab stores the numbers in matrix
        #format while in our case of python it is being stored as str
        tmplist = []
        for j in range(len(lst[i])):
            sign = pow(-1,int(lst[i][j]))
            tmplist.append(sign)
            # print(sign)
        signs.append(tmplist)
        print("*******************************************************")
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
        print(H_B.shape)
        poly = cdd.Polyhedron()
    # print(type(lst[1]))


    # for i in range(10):
    #     b = bin(i)
    #     print(b)


