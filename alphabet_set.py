from read_data import ReadData
import numpy as np

alphabet = ReadData.alphabet

def Find1inStrofArray(list):
    ind = []
    counter = 0
    for x in list:
        if x == '1':
            counter = counter + 1
            ind.append(counter)
        else:
            counter = counter +1
    return ind



class Alphs_set:
    N_p = len(alphabet)-1
    Alph_s = []
    # note that I am staring from 1 instead of 0
    for i in range(1,pow(2,N_p)):
        lst = []
        a = format(i, 'b')
        addZeros = 10 - len(a)
        string_val = "".join('0' for i in range(addZeros))  # this is our s
        lst.append(string_val + a)  # this is equivalent to matlab dec2bin except matlab stores the numbers in matrix
        # print(lst)
        # index = np.nonzero(np.asarray(lst[i-1]))
        # print(lst[i-1])
        index = Find1inStrofArray(lst[0])

        tmp = "".join(alphabet[i-1] for i in index)
        Alph_s.append(tmp)

    Alph_s.append(alphabet[len(alphabet)-1])
    # print(Alph_s)
    # print(len(Alph_s))