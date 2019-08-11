from src.trans_sys_polytope import TransSysToPolytope as TransSys
from src.autom_product import AutomProduct as product

# class to find all possible initial states of Tp from which there
# there exists a run satisfying the LTL formula represented by Buchi Automaton B

accept_Q0 = []
accept_run = []

class Accepted_Q0:
    Tp_Q = TransSys.Tp_Q
    for i in Tp_Q:
        Tp_Q0 = i
        P_S = product.P_S
        P_F = product.P_trans
        P_S0 = product.P_S0
        P_F = product.P_F