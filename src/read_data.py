from array import array
import sys
import numpy  as np

class ReadData:
# def ReadData():


    def __init__(self):
        self

    def readdata(self):

        print("See examples (readme.txt); the correctness of input data is not "
              "extesively checked! All restriction are of type Ax + b (<=) 0 \n")
        read_file = input("Read data from a file? Y/N \n")

        """looks like you can  not ask user to input array because they will be inputed as strings and thus saving it in file and loading might not work. For now lets write a alternate case of reading arrays form txt files"""
        # u = np.arange(10)
        # aaa = np.ndarray((2,2))
        # print(aaa.ndim)

        # a = np.array([[2,1],[2,1]])
        # b = np.array([2,2])
        # print(a.transpose(),b)
        # a = np.array(input("Enter the fucking 2d matrix \n"))
        # b = np.array(input("Enter the fucking 1d matrix \n"))
        # print(a.shape)
        # list = (a,'str',3)
        # tmpList = []
        # tmpList.append(np.asarray(a))
        # tmpList.append(b)
        # tmpList.append('str')
        # tmpList.append(4)
        # for i in list:
        #       print(type(i))
        # print("*********************")
        # for i in tmpList:
        #       print(type(i))
        # print(list[0].transpose())
        # print(a.ndim)
        # print("jkdksdkb " + str(b.ndim))
        # x,y = np.shape(a)
        # print(x)
        # print(y)


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
                    print(type(A[i]))
                    #print(str(np.size(A[])))
                    #B.append(input("Vector B" + str(i + 1) + "(" + str(A[,:].size) + "x 1) for proposition" + str(i + 1) + "\n"))
                #TODO add try and catch for accepting valid matrix types in A and for B
                alphabet.append("p"+str(N_p+1)) # did not get exactly why this is being done
                A.append(np.array(input("Matrix (m" + str(N_p+1)+"x"+str(n)+") for state space boundaries \n" )))
                # print("A is fine")
                tmp = A.__getitem__(N_p)  # already a
                tmp1= A.__getitem__(0)
                # print(tmp[0])
                print(type(tmp))
                print(tmp.reshape(1,1))
                print(tmp.ndim)
                print(tmp1.ndim)
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

        else:
            # testList = []
            # A = np.ndarray
            # csv_fname = 'test.txt'
            # with open(csv_fname) as fp:
            #     for line in fp:
            #         element = int(float(elt.strip()) for elt in line.split(','))
            #         A.__add__(element)
            #         testList.append(element)
            #     print(testList)


            #     fp.write("""\
            # "A","B","C","D","E","F","timestamp"
            # 611.88243,9089.5601,5133.0,864.07514,1715.37476,765.22777,1.291111964948E12
            # 611.88243,9089.5601,5133.0,864.07514,1715.37476,765.22777,1.291113113366E12
            # 611.88243,9089.5601,5133.0,864.07514,1715.37476,765.22777,1.291120650486E12
            # """)



            # Read the CSV file into a Numpy record array

            #r = np.genfromtxt(csv_fname,float,'#',',')
            # r = np.genfromtxt("test.csv",array,'#')

            n = 2
            N_p = 10
            orig_alph = ['p1','p2','p3','p4','p5','p6','p7','p8','p9','p10','p11'] #just check how many these do you need
            alphabet = ['p01', 'p02', 'p03', 'p04', 'p05', 'p06', 'p07', 'p08', 'p09', 'p10', 'p11'] #it will ave the same number as above with naming scheme changed
            A = [np.array([0,1]),np.array([1,-1]),np.array([4,1]),np.array([4,-7]),np.array([-2,-1]),np.array([-1,-12]),np.array([-1,-1]),np.array([1,0]),np.array([0,-1]),np.array([-6,4.5]),
                 np.array([[-1,0],[1,0],[0,-1],[0,1],[-3,-5],[1,-1],[-1,2.5],[-2,2.5]])]
            # A = np.array([[0,1],[1,-1],[4,1],[4,-7],[-2,-1],[-1,-12],[-1,-1],[1,0],[0,-1],[-6,4.5],[[-1,0],[1,0],[0,-1],[0,1],[-3,-5],[1,-1],[-1,2.5],[-2,2.5]]])
            B = [np.array([0]),np.array([0]),np.array([12]),np.array([34]),np.array([4]),np.array([31]),np.array([11]),np.array([-3]),np.array([-1.5]),np.array([-12]),np.array([[-5],[-7],[-3],[-6],[-15],[-7],[-15],[-17.5]])]
            D_A = np.array([[0.2,-0.3],[0.5,-0.5]])
            D_b = np.array([[0.5], [0.5]])
            D_B = np.array([[1, 0], [0, 1]])
            U_A = np.array([[1, 0], [0, 1], [-1, 0], [0, -1]])
            U_b = np.array([[-2],[-2],[-2],[-2]])
            # use this guy in future - np.concatenate

            # print(A,"\n")
            # print(B,"\n")
            # print(D_B,"\n")
            # print(D_A,"\n")
            # print(D_b,"\n")
            # print(U_A,"\n")
            # print(U_b,"\n")

            # print(ReadData.D_b.shape)

        return n, A, B, U_A, U_b, D_A, D_B, D_b, alphabet, orig_alph

if __name__ == "__main__":
    tmp = ReadData()
    tmp.readdata()
