from src.trans_sys_polytope import TransSysToPolytope as TransSys
from src.autom_product import AutomatonProduct as product
from src.invalidate_transitions import Invalid_Transition
from src.find_accepted_run import FindRuns
import src.plt_tr_sys_polyt as trans_plot

# class to find all possible initial states of Tp from which there
# there exists a run satisfying the LTL formula represented by Buchi Automaton B


# Tp_adj = Invalid_Transition.updated_Tp_adj

def pltfig():
    print("Plotting figures")
    # # trans_plot.PlotTraSys(True, accepted_Q0= Accepted_Q0.accept_Q0)
    # ax = trans_plot.plt
    # ax.show()


class Accepted_Q0:

    def __init__(self, Tp, B):
        self.Tp = Tp
        self.B = B

    def acceptedQ0(self):

        Tp = self.Tp
        B = self.B

        Tp_Q = Tp.get("Tp.Q")


        accept_Q0 = []
        accept_run = []
        flag = 0
        # Tp_Q = TransSys.Tp_Q
        no_of_states = len(Tp_Q)
        for i in Tp_Q:
            Tp_Q0 = i
            P_F, P_S0, P_S, P_trans = product(Tp, B, Tp_Q0, flag, no_of_states)

            flag = flag + 1
            # Tp_adj = updated_Tp_adj
            run_tp = FindRuns(P_F,P_S0,P_S,P_trans)
            if not isinstance(run_tp, type(None)):
                if len(accept_Q0) == 0:
                    print("Indices of Initial states of transition system on polytopes from which LTL formula "
                          "can be satisfied: \n")

                accept_Q0.append(i)
                accept_run.append(run_tp)
                print(i)
            # if i == (len(Tp_Q) - 1):
            #     # pltfig()
            #     print("Plotting figures")
            #     # trans_plot.PlotTraSys(True, accepted_Q0=accept_Q0)
            #
            #     ax = trans_plot.plt
            #     ax.show()

        print("\n")

        # if i == len(Tp_Q):
        #     # plot.nargmin = True
        #     trans_plot.PlotTraSys(True)
        #     ax = trans_plot.plt
        #     ax.show()


        if len(accept_Q0) == 0:
            print("There are no initial states from which the LTL formula can be satisfied \n")
            # P_S = product.P_S
            # P_F = product.P_trans
            # P_S0 = product.P_S0
            # P_F = product.P_F
        return accept_Q0, accept_run

def getAccept_Q0():
    return Accepted_Q0.accept_Q0


