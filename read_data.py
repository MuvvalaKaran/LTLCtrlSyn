from array import array
import sys
import numpy  as np

print("See examples (readme.txt); the correctness of input data is not "
      "extesively checked! All restriction are of type Ax + b (<=) 0 \n")
read_file = input("Read data from a file? Y/N \n")

u = np.arange(10)
aaa = np.ndarray((2,2))
print(aaa.ndim)

DEBUG = True
if read_file  == 'N' or read_file == 'n':
        #print("reading from file")
        # TODO add valid try and catch exception for entring ints and strs at appropriate places
        n = int(input("Space dimension \n"))
        N_p = int(input("Number of atomic proposition(observable) : \n"))
        pad_no = len(str(N_p+1)) #if N_p < 10 then one and >= 10 then 2 and so on for higher no. of propositoins


        orig_alph = [] # its declared as a list
        alphabet = []  # this is declared as a list too
        A = [] # lets create a list of array
        B = [] #
        # x = []
        #A = np.ndarray(shape=())
        for i in range(N_p):

            orig_alph.append(str("p"+str(i + 1))) #original alphabet of type p1
            #print(orig_alph[i])
            if N_p >= 10:
                if i+1<10:
                    alphabet.append("p"+str(0)+str(i+1)) #alphabet of type p01
                else:
                    alphabet.append("p"+str(i+1))
            else:
                alphabet.append("p" + str(i+1)) # enter else loop if a.p is less than 10 and the above format is not required
            #A[i] = np.asmatrix(np.array(input("Matrix A"+str(i + 1)+ "(m"+str(i + 1)+ "x"+ str(n)+ ") for proposition"+ str(i + 1)+"\n")))
            #x = np.ndarray((1,n),float)
            x = np.array(input("Matrix A" + str(i + 1) + "(m" + str(i + 1) + "x" + str(n) + ") for proposition" + str(i + 1) + "\n"))
            A.append(x)
            #A.append(np.array(input("Matrix A"+str(i + 1)+ "(m"+str(i + 1)+ "x"+ str(n)+ ") for proposition"+ str(i + 1)+"\n")))
            y = np.array(input("Vector B"+str(i + 1)+ "("+str(np.size(A[i]))+ "x 1) for proposition"+ str(i + 1)+"\n"))
            B.append(y)
            #B.append(input("Vector B"+str(i + 1)+ "("+str(len(A[i]))+ "x 1) for proposition"+ str(i + 1)+"\n"))
            print(A[i])
            #print(str(np.size(A[])))
            #B.append(input("Vector B" + str(i + 1) + "(" + str(A[,:].size) + "x 1) for proposition" + str(i + 1) + "\n"))
        #TODO add try and catch for accepting valid matrix types in A and for B
        alphabet.append("p"+str(N_p+1)) # did not get exactly why this is being done
        A.append(np.array(input("Matrix (m" + str(N_p+1)+"x"+str(n)+") for state space boundaries \n" )))
        # print("A is fine")
        tmp = A.__getitem__(N_p)  # already a
        print(tmp[0])
        print(type(tmp))
        print(tmp.reshape(1,1))
        print(tmp.ndim)
        #print(np.shape(np.asarray(tmp)))
        # a = np.array([2 2; 2 2])
        B.append(np.array(input("Vector (" + str(np.ndim(tmp)) + " X 1) for state space boundaries \n")))
        # B[N_p +1] = np.array(input("Vector (" + str(len(A[N_p+1])) + "X 1) for state space boundaries \n"))
        # A.append(input("Matrix (m" + str(int(N_p)+1)+"x"+str(n)+") for state spae boundaries \n" ))
        # print(len(A[int(N_p)]))

        if(DEBUG):
            print(type(A[0]))
            for element in A:
                print(element)
        # B.append(input("Vector (" + str(len(A[int(N_p)])) + "X 1) for state space boundaries \n"))
        print("Dynamics are given by: dot(x) = D_A x + D_B u + D_b \n")
        m = int(input("Number of controls(dim of space in which u lives): "))
        D_A = np.array(input("Matrix D_A (" + str(n) + "x " + str(n) +") : \n" ))
        D_B = np.array(input("Matrix D_B (" + str(n) + "x " + str(m) +") : \n" ))
        D_b = np.array(input("Column Vector D_b (" + str(n) + "x 1) : \n" ))
        U_A = np.array(input("Matrix U_A ( m_u x " + str(m) + ", m_u > " + str(m) +")defining bounded polytope containing speed boundaries: \n" ))
        U_b = np.array(input("Column Vector U_b ( " + str(np.size(U_A[:,1])) + "X 1) corresponding to matrix U_A: \n"))
