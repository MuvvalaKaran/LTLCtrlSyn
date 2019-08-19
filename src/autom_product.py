from src.trans_sys_polytope import TransSysToPolytope as Trans_Sys
from src.invalidate_transitions import Invalid_Transition
# from src.accepted_init_states import Accepted_Q0
# from src.cartesian_product import Cartesian_product
import src.create_buchi as Buchi
import numpy as np

# performs the product of 2 automaton
# first automaton (T) is in fact a finite transition system with observables
# (a state has ONLY one observable - a label from set of subsets of all possible observables - see alphabet_set & trasition system for sub-polytopes construction)
# second one (B) is one with guards on transitions (in this case a Buchi automata)
# a guard can be any combination of observables (as they would have "or" between them) - any subset of sets of alphabet_set
# (the alphabet of B (set of guards) is (must be) included (or equal) in the set of observations of T, given by alphabet_set)
# T and B are implemented as structures (see functions trans_sys_polytope and create_buchi, which construct T and B, respectivelly)
#
# T has fields Q, Q0, obs, adj(from invalidate_trans) (set of observables is 1:length(alphabet_set))
# B has fields S, S0, F, trans
# P is the product automaton
#
# a dummy initial state will be temporarly added to T (in order to check if parts of formula are verified (or whole formula is false) from start)
# the dummy state has transitions only to initial states of T and no state has transitions to it
# the dummy state is the last (has the biggest label), has no observable and no vertices
# when a run is searched in the product automaton, the first state (the dummy one) will be removed

def ismember(a, b):
    # bind = {}
    # for i, elt in enumerate(b):
    #     if elt not in bind:
    #         bind[elt] = i
    # return [bind.get(itm, None) for itm in a]  # None can be replaced by any other "not in b" value
    # ret = []
    for counter, i in enumerate(b):
        ret = False
        if a == i:
            # ret.append(counter)
            ret = True
            break
    return ret

def CartesianProduct(Tp_Q, B_S):
    varargin = []
    N = []
    number_of_arg = 2
    is_arg1Scalar = False
    is_arg2Scalar = False
    if isinstance(Tp_Q, type(None)):
        set = []
    if isinstance(B_S, type(None)):
        set = []
    varargin.append(Tp_Q)
    varargin.append(B_S)
    try :
        N.append(len(varargin[0]))
    except:
        N.append(1)
        is_arg1Scalar = True
    try:
        N.append(len(varargin[1]))

    except:
        N.append(1)
        is_arg2Scalar = True

    N.insert(0, 1)
    N.append(1)

    set = np.zeros((np.prod(N), number_of_arg))

    loop_over_reverse = np.arange(number_of_arg,0,-1)
    for i in loop_over_reverse:
        i = i - 1  # hack for the reverse loop to sync with indices
        col = []
        if(is_arg1Scalar == True or is_arg2Scalar ==True):
            # j = 0
            tmp = np.tile(varargin[i], (np.prod(N[i + 2:len(N)]), 1))
            if (tmp.size == 1):
                col.append(tmp[0][0])
                use = 1
            else:
                col.append(np.tile(varargin[i], (np.prod(N[i + 2:len(N)]), 1)))
                use = 2
            # col.appen np.tile(varargin[i][j], (np.prod(N[i+2:len(N)]), 1))
            # col.append(tmp)
            if (use == 1):
                init_len = len(col)
                tmp = list(np.tile(col, (np.prod(N[0:i + 1]), 1)))
                tmp = [item for sublist in tmp for item in sublist]
                col.append(tmp)  # as N is a list and slicing end element should + 1
                col = [item for sublist in col[init_len:] for item in sublist]
                # col = [item for sublist in col for item in sublist]
                # print("slkcjs")
                set[:, i] = col
            elif (use == 2):
                col = [array.tolist() for array in col]
                col = [item for sublist in col for item in sublist]
                col = [item for sublist in col for item in sublist]
                set[:, i] = col

        else:
            for j in range(len(varargin[i])):

                tmp = np.tile(varargin[i][j], (np.prod(N[i + 2:len(N)]), 1))
                if (tmp.size == 1):
                    col.append(tmp[0][0])
                    use = 1
                else:
                    col.append(np.tile(varargin[i][j], (np.prod(N[i+2:len(N)]), 1)))
                    use = 2
                # col.appen np.tile(varargin[i][j], (np.prod(N[i+2:len(N)]), 1))
                # col.append(tmp)
            if(use == 1):
                init_len = len(col)
                tmp = list(np.tile(col, (np.prod(N[0:i + 1]), 1)))
                tmp = [item for sublist in tmp  for item in sublist]
                col.append(tmp)  # as N is a list and slicing end element should + 1
                col = [item for sublist in col[init_len:] for item in sublist]
                # col = [item for sublist in col for item in sublist]
                # print("slkcjs")
                set[:,i] = col
            elif(use ==2):
                col = [array.tolist() for array in col]
                col = [item for sublist in col for item in sublist]
                col = [item for sublist in col for item in sublist]
                set[:,i] = col

    return set



# class AutomProduct:
def AutomatonProduct(Tp, B, Tp_Q0, flag, count):


    B_S = B.get("B.S")
    B_S0 = B.get("B.S0")
    B_F = B.get("B.F")
    B_trans = B.get("B.trans")

    counter_for_to_maintain_Tp_size = flag
    # B_S = Buchi.B_S
    # B_S0 = Buchi.B_S0
    # B_F = Buchi.B_F
    # B_trans = Buchi.B_trans1

    Tp_Q0 = Tp_Q0
    _Tp_Q = Tp.get("Tp.Q")[0:count]
    # Tp_Q = Tp_Q
    Tp_obs = Tp.get("Tp.obs")
    Tp_adj = Tp.get("Tp.adj")

    # Tp_Q0 = Accepted_Q0.Tp_Q0
    # Tp_Q0 = Tp_Q0
    # _Tp_Q = Trans_Sys.Tp_Q[0:count]
    # # Tp_Q = Tp_Q
    # Tp_obs = Trans_Sys.Tp_obs
    # Tp_adj = Invalid_Transition.updated_Tp_adj

    Debug = True

    if Debug:
        Tp_adj = np.zeros((33,33))
        Tp_adj[0,0] = 1
        Tp_adj[1, 0] = 1
        Tp_adj[2, 0] = 1
        Tp_adj[0, 1] = 1
        Tp_adj[1, 1] = 1
        Tp_adj[3, 1] = 1
        Tp_adj[14, 1] = 1
        Tp_adj[0, 2] = 1
        Tp_adj[2, 2] = 1
        Tp_adj[3, 2] = 1
        Tp_adj[4, 2] = 1
        Tp_adj[9, 2] = 1
        Tp_adj[25, 2] = 1
        Tp_adj[1,3] = 1
        Tp_adj[2,3] = 1
        Tp_adj[3,3] = 1
        Tp_adj[26,3] = 1
        Tp_adj[2,4] = 1
        Tp_adj[4,4] = 1
        Tp_adj[5,5] = 1
        Tp_adj[6,5] = 1
        Tp_adj[9,5] = 1
        Tp_adj[8,7] = 1
        Tp_adj[11,8] = 1
        Tp_adj[2,9] = 1
        Tp_adj[9,9] = 1
        Tp_adj[32,9] = 1
        Tp_adj[4,10] = 1
        Tp_adj[12,13] = 1
        Tp_adj[17,13] = 1
        Tp_adj[13,14] = 1
        Tp_adj[14,14] = 1
        Tp_adj[26,14] = 1
        Tp_adj[15,15] = 1
        Tp_adj[15,16] = 1
        Tp_adj[16,17] = 1
        Tp_adj[18,18] = 1
        Tp_adj[21,18] = 1
        Tp_adj[27,18] = 1
        Tp_adj[19,19] = 1
        Tp_adj[20,19] = 1
        Tp_adj[21,19] = 1
        Tp_adj[22,19] = 1
        Tp_adj[23,19] = 1
        Tp_adj[28,19] = 1
        Tp_adj[17,20] = 1
        Tp_adj[19,20] = 1
        Tp_adj[20,20] = 1
        Tp_adj[18,21] = 1
        Tp_adj[19,21] = 1
        Tp_adj[21,21] = 1
        Tp_adj[29,21] = 1
        Tp_adj[19,22] = 1
        Tp_adj[22,22] = 1
        Tp_adj[25,22] = 1
        Tp_adj[30,22] = 1
        Tp_adj[19,23] = 1
        Tp_adj[23,23] = 1
        Tp_adj[25,23] = 1
        Tp_adj[20,24] = 1
        Tp_adj[23,24] = 1
        Tp_adj[2,25] = 1
        Tp_adj[22,25] = 1
        Tp_adj[23,25] = 1
        Tp_adj[25,25] = 1
        Tp_adj[26,25] = 1
        Tp_adj[32,25] = 1
        Tp_adj[3,26] = 1
        Tp_adj[17,26] = 1
        Tp_adj[24,26] = 1
        Tp_adj[25,26] = 1
        Tp_adj[26,26] = 1
        Tp_adj[18,27] = 1
        Tp_adj[27,27] = 1
        Tp_adj[29,27] = 1
        Tp_adj[19,28] = 1
        Tp_adj[28,28] = 1
        Tp_adj[29,28] = 1
        Tp_adj[30,28] = 1
        Tp_adj[21,29] = 1
        Tp_adj[27,29] = 1
        Tp_adj[28,29] = 1
        Tp_adj[29,29] = 1
        Tp_adj[31,29] = 1
        Tp_adj[5,30] = 1
        Tp_adj[22,30] = 1
        Tp_adj[28,30] = 1
        Tp_adj[30,30] = 1
        Tp_adj[32,30] = 1
        Tp_adj[7,31] = 1
        Tp_adj[30,31] = 1
        Tp_adj[9,32]  = 1
        Tp_adj[25,32] = 1
        Tp_adj[30,32] = 1
        Tp_adj[32,32] = 1




    # Tp_adj = Tp_adj
    st_no_T = len(_Tp_Q)
    if(counter_for_to_maintain_Tp_size == 0):
        _Tp_Q.append(st_no_T)
        # counter_for_to_maintain_Tp_size = counter_for_to_maintain_Tp_size + 1
    else:
        #_Tp_Q[35] = st_no_T
        _Tp_Q.append(st_no_T)
    # print(Tp_Q)
    # tmp = np.zeros((1,st_no_T))

    Tp_adj = np.vstack((Tp_adj,np.zeros((1, st_no_T))))
    Tp_adj = np.hstack((Tp_adj, np.transpose(np.zeros((1, st_no_T + 1)))))  # no state can transit in dummy one
    Tp_adj[st_no_T, Tp_Q0] = 1 # add transition to initial state
    Tp_Q0 = st_no_T # new initial state

    #call a class called cartesian product
    P_S = CartesianProduct(Tp_Q=_Tp_Q, B_S=B_S)
    init_st = CartesianProduct(Tp_Q=Tp_Q0,B_S=B_S0)
    fin_st = CartesianProduct(_Tp_Q[0:st_no_T], B_F)

    P_S0 = []
    P_F = []

    for i in range(np.shape(init_st)[0]):
        # np.where(
        counter = 0
        match_index = []
        for index in range(np.shape(P_S)[0]):
            if (P_S[index,0] == init_st[i,0]) and (P_S[index,1] == init_st[i,1]):
                match_index.append(counter)
            counter = counter + 1

        P_S0.append(match_index)

    for i in range(np.shape(fin_st)[0]):
        # np.where(
        counter = 0
        match_index = []
        for index in range(np.shape(P_S)[0]):
            if (P_S[index,0] == fin_st[i,0]) and (P_S[index,1] == fin_st[i,1]):
                match_index.append(counter)
            counter = counter + 1

        P_F.append(match_index)

    P_trans = np.zeros((np.shape(P_S)[0], np.shape(P_S)[0]))
    # tr_q = []
    # tr_s = []
    for i in range(np.shape(P_S)[0]):
        tr_q = np.nonzero(Tp_adj[int(P_S[i,0]),:])
        tr_s = np.nonzero(B_trans[int(P_S[i,1])][:])
        if np.size(tr_q) == 0 or np.size(tr_s) == 0:
            continue
        # abcderfg = np.shape(tr_q)[0]
        # if np.shape(tr_q)[0] != 0:
        for j in range(len(tr_q[0])):
            # if np.shape(tr_s)[0] != 0:
                for k in range(len(tr_s[0])):
                    # if not isinstance(B_trans[int(P_S[i,1])][tr_s[0][k]] , type(None)):
                    # if np.shape(tr_q)[0] == 0 or np.shape(tr_s)[0] == 0:
                    #     break
                    # else:
                    if ismember(int(Tp_obs[0][tr_q[0][j]]) , B_trans[int(P_S[i,1])][tr_s[0][k]]):
                        # ind = []
                        # tmp_counter = 0
                        for tmp_i in range(np.shape(P_S)[0]):
                            if ((int(P_S[tmp_i,0]) == tr_q[0][j])  and int(P_S[tmp_i,1]) == tr_s[0][k]):
                                # ind = tmp_counter
                                P_trans[i, tmp_i] = 1
                            # tmp_counter = tmp_counter + 1

    # print("Done")

    return P_F,P_S0,P_S,P_trans

