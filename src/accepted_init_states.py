from src.trans_sys_polytope import TransSysToPolytope as TransSys
from src.autom_product import AutomatonProduct as product
from src.invalidate_transitions import Invalid_Transition
from src.find_accepted_run import FindRuns

# class to find all possible initial states of Tp from which there
# there exists a run satisfying the LTL formula represented by Buchi Automaton B

accept_Q0 = []
accept_run = []
# Tp_adj = Invalid_Transition.updated_Tp_adj
flag = 0
Tp_Q = TransSys.Tp_Q
no_of_states = len(TransSys.Tp_Q)

class Accepted_Q0:
    hmm = []
    for i in Tp_Q:
        Tp_Q0 = i
        P_F, P_S0, P_S, P_trans = product(Tp_Q0, flag, no_of_states)
        hmm.append(P_trans)
        flag = flag + 1
        # Tp_adj = updated_Tp_adj
        run_tp = FindRuns(P_F,P_S0,P_S,P_trans)
        # P_S = product.P_S
        # P_F = product.P_trans
        # P_S0 = product.P_S0
        # P_F = product.P_F
    # print(hmm)