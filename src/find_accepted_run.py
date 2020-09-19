from src.find_paths import FindPaths
import numpy as np


def findtheshortestlistWInd(multilist):
    min = np.Inf
    ret = 0
    for counter, sublist in enumerate(multilist):
        if len(sublist) < min:
            min = len(sublist)
            ret = counter
    return min, ret


def findemptycellsinlist(list):
    #  we assign 1s to cells where are empty
    for index,i in enumerate(list):
        #i itself is a sublist(cell)
        if len(i) != 0:
            if i == 1:
                list[index] = 1
    return list


def FindRuns(P_F, P_S0, P_S, P_trans):
    """
    find an accepted run of product automaton P and project it to states of Tp

    :param P_F:
    :param P_S0:
    :param P_S:
    :param P_trans:
    :return: The run with the shortest prefic and shortest suffix for the prefix
    A cell array with 2 elements :
        first (prefix) is a vector starting from initial state and containing a run (up to a final state, fs),
        second (suffix) is a vector containing a path which must be repeated infinitely (it starts with a neighbor of fs
         - last state from prefix - and it ends with fs)
    """

    # run_P = np.arange(0, len(P_S0))
    run_P = []
    for i in range(len(P_S0)):
        prefix = FindPaths(P_trans,P_S0[i],P_F)
        # new_prefix = np.nonzero(findemptycellsinlist(prefix))
        prefix = [sublist for sublist in prefix if len(sublist) != 0]
        # prefix = [int(item) for sublist in prefix for item in sublist]
        for sublist in range(len(prefix)):
            for item in range(len(prefix[sublist])):
                prefix[sublist][item] = int(prefix[sublist][item])

        # print("In Find runs", prefix)
        # sh_p = [] # a list to stor prefix lengths
        # ind = np.arange(0,len(prefix))
        ind = []
        if len(prefix) != 0:
            sh_p = sorted(prefix, key=len)
            # ind.append([len(i) for i in prefix])
            # ind = [item for sublist in ind for item in sublist]
            ind = list(range(len(prefix)))
            # a, ind = findtheshortestlistWInd(prefix)
            for j in ind:
                suffix = []
                if P_trans[prefix[j][-1],prefix[j][-1]] == 1:
                    suffix = int(prefix[j][-1])
                else:
                    neigh = []
                    for loop_index in range(len(P_trans[0])):
                        if P_trans[loop_index, prefix[j][-1]] == 1:
                            neigh.append(loop_index)

                    if not isinstance(neigh, type(None)):
                        suffix = FindPaths(P_trans, prefix[j][-1], neigh)
                        suffix = [sublist for sublist in suffix if len(sublist) != 0]
                        for sublist in range(len(suffix)):
                            for item in range(len(suffix[sublist])):
                                suffix[sublist][item] = int(suffix[sublist][item])

                        # sh_s = []
                        # ind_suf = np.arange(0,len(suffix)) # need to add a if to avoid len being 0
                        # if not isinstance(suffix, type(None)):
                        if len(suffix) != 0:
                            # sh_s = suffix.sort(key=len)
                            # ind_suf = ind_suf[0]
                            sh_s, ind_suf = findtheshortestlistWInd(suffix)
                            tmp = suffix[ind_suf][1:]
                            tmp.append(suffix[ind_suf][0])
                            suffix = tmp
                if len(suffix) != 0:
                    if not isinstance(suffix[0],type(None)):
                        run_P.insert(i, [prefix[j]] + [suffix])  #maybe declare run_p as a list
                        break

    run_P = [sublist for sublist in run_P if len(sublist) != 0]

    if len(run_P) == 0:
        run_Tp = []
        #break # its a return here
        return

    run_Tp = []
    length_Pre_suff = []
    run_length = []
    for i in range(len(run_P)):
        for k in range(len(run_P[i])):
            length_Pre_suff.append(len(run_P[i][k]))

    run_length.append(np.sum(length_Pre_suff))

    # r_l = []
    # ind = np.arange(0,len(run_length))
    ind = list(range(0,len(run_length)))
    r_l = np.amin(run_length)
    # run_Tp.append([P_S[slice(run_P[ind][0][1:]), 1]])#, P_S[slice(run_P[ind][1]), 1]])
    prefix_run_tp = []
    suffix_run_tp = []
    for append_ind in range(len(run_P[ind[0]][0])):
        if append_ind > 0:
            prefix_run_tp.append(P_S[run_P[ind[0]][0][append_ind], 0])

    for append_ind in range(len(run_P[ind[0]][1])):
        suffix_run_tp.append(P_S[run_P[ind[0]][1][append_ind], 0])

    run_Tp.append([prefix_run_tp, suffix_run_tp])

    return run_Tp







