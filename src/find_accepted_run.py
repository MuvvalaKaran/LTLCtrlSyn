from src.find_paths import FindPaths

import numpy as np



#  find an accepted run of product automaton P and project it to states of Tp (we need a run for Tp satisfying the LTL formula)
#  run_Tp will be a cell array with 2 elements: first (prefix) is a vector starting from initial state and containing a run (up to a final state, fs),
#  second (suffix) is a vector containing a path which must be repeated infinitely (it starts with a neighbor of fs - last state from prefix - and it ends with fs)
#  (if the suffix has just an element (fs), then fs has a loop in itself, which will be repeated infinitely often)
#  the returned run_Tp will be the run with the shortest prefix and shortest suffix for that prefix

def findemptycellsinlist(list):
    #  we assign 1s to cells where are empty
    for index,i in enumerate(list):
        #i itself is a sublist(cell)
        if len(i) != 0:
            if i == 1:
                list[index] = 1
    return list

def FindRuns(P_F,P_S0,P_S,P_trans):
    run_P = np.arange(0, len(P_S0))
    for i in range(len(P_S0)):
        prefix = FindPaths(P_trans,P_S0[i],P_F)
        new_prefix = np.nonzero(findemptycellsinlist(prefix))
        print("In Find runs" , prefix)

        if len(prefix[0]) != 0:
            print("Hey This is my first prefix")

