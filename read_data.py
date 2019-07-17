from array import array
import sys

print("See examples (readme.txt); the correctness of input data is not "
      "extesively checked! All restriction are of type Ax + b (<=) 0 \n")
read_file = input("Read data from a file? Y/N \n")

if read_file  == 'N' or read_file == 'n':
        #print("reading from file")
        # TODO add valid try and catch exception for entring ints and strs at appropriate places
        n = input("Space dimension \n")
        N_p = input("Number of atomic proposition(observable) : \n")
        pad_no = str(len(str(int(N_p)+1))) #if N_p < 10 then one and >= 10 then 2 and so on for higher no. of propositoins


        orig_alph = [] # its declared as a list
        alphabet = []  # this is declared as a list too
        A = [] #
        B = [] #
        x = []
        for i in range(int(N_p)):

            orig_alph.append(str("p"+str(i + 1))) #original alphabet of type p1
            #print(orig_alph[i])
            if int(N_p) >= 10:
                if i+1<10:
                    alphabet.append("p"+str(0)+str(i+1)) #alphabet of type p01
                else:
                    alphabet.append("p"+str(i+1))
            else:
                alphabet.append("p" + str(i+1)) # enter else loop if a.p is less than 10 and the above format is not required
            A.append(input("Matrix A"+str(i + 1)+ "(m"+str(i + 1)+ "x"+ str(n)+ ") for proposition"+ str(i + 1)+"\n"))
            B.append(input("Vector B"+str(i + 1)+ "("+str(len(A[i]))+ "x 1) for proposition"+ str(i + 1)+"\n"))
        #TODO add try and catch for accepting valid matrix types in A and for B
        alphabet.append("p"+str(int(N_p)+1)) # did not get exactly why this is being done
        # A[int(N_p+1)] = input("Matrix (m" + str(int(N_p)+1)+"x"+str(n)+") for state spae boundaries \n" )
        # B[int(N_p +1)] = input("Vector (" + str(len(A[int(N_p)+1])) + "X 1) for state space boundaries \n")
        A.append(input("Matrix (m" + str(int(N_p)+1)+"x"+str(n)+") for state spae boundaries \n" ))
        print(len(A[int(N_p)]))
        print(A)
        B.append(input("Vector (" + str(len(A[int(N_p)])) + "X 1) for state space boundaries \n"))
        #print(A)
        print(B)