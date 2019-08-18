import numpy as np

# Use_mine = True
# X0 = input("Enter Initial continuous state x0 (column vector) 2 x 1")
# if Use_mine:
#     X0 = np.array([[-4], [1]])
def ismember(a, b):
    for counter, i in enumerate(b):
        ret = False
        if a == i:
            # ret.append(counter)
            ret = True
            break
    return ret

def findInitState(A,b,x0,signs, acceptQ0):
    Ain = [A[:-1]]
    Bin = [b[:-1]]
    Ain = Ain[0]  # as its a list which is a collection of arrays
    Bin = Bin[0]
    sp_no= np.shape(signs)[0]
    v0 = np.transpose(np.matmul(Ain, x0) + Bin)

    # for i in range(len(np.shape(signs)[0])):
    #     signs[i, np.nonzero(v0)] = []
    for i in range(len(signs)):  # will be a 1d array
        index = (np.argwhere(v0 == 0))
        index = index.tolist()
        for sub_i in index:
            signs[i][sub_i] = []

    index = np.argwhere(v0 == 0)
    index = index.tolist()
    for sub_i in index:
        v0[sub_i] = []

    # s0 = [1 for i in v0[0] if i > 0]
    s0 = []
    for i in v0[0]:
        if i > 0:
           s0.append(1)
        else:
            s0.append(0)

    copy = np.tile(s0,(sp_no, 1))
    # equal = np.argwhere(copy == signs)  # this might not work now
    equal = []
    for row in range(len(signs)):
        equal_row = []
        for element_signs,element_copy in zip(signs[row],copy[row]):
            if element_copy == element_signs:
                equal_row.append(1)
            else:
                equal_row.append(0)
        equal.append(equal_row)

    q0 = []
    for counter,row in enumerate(equal):
        row_sum = np.sum(row)
        if row_sum == len(s0):
            q0.append(counter)


    # if isinstance(q0, type(None)):
    if len(q0) == 0:
        q0 = []
        return
    elif len(q0) > 1:
        for i in range(len(q0)):
            if ismember(q0[i], acceptQ0):
                q0 = q0[i]
                break
            else:
                q0 = q0[0]
    return q0






