from read_data import ReadData
import numpy as np

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
            signs = pow(-1,int(lst[i][j]))
            tmplist.append(signs)
            print(signs)
        signs.append(tmplist[i])
        print("*******************************************************")
        # H = np.array(np.diag(np.diag(signs))*Ain)
    # print(type(lst[1]))


    # for i in range(10):
    #     b = bin(i)
    #     print(b)


