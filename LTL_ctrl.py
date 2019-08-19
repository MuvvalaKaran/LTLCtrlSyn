# the main class that will be used to call things
import src.find_init_state as find_init_state
import src.trans_sys_polytope as trans_sys_polytope
import src.accepted_init_states as accepted_init_state
import src.invalidate_transitions as invalidate_transitions
import src.control_sequence as control_sequence
import src.plt_tr_sys_polyt as plt_tr_sys_polyt
import src.alphabet_set as alphabet_set
import src.read_formula as read_formula
import src.create_buchi as create_buchi
import src.plot_drift as plot_drift
import src.read_data as read_data
import src.plot_run as plot_run
import src.plot_trajectory as plot_trajectory
import src.simulate_system as simulate_system
import os
import numpy as np


def ismember(__a, __b):
    for counter, i in enumerate(__b):
        ret = False
        if __a == i:
            # ret.append(counter)
            ret = True
            break
    return ret


[n, A, b, U_A, U_b, D_A, D_B, D_b, alphabet, orig_alph] = read_data.ReadData()

start = os.times()[4]
Tp = trans_sys_polytope.TransSysToPolytope(A, b)
stop = os.times()[4]

print("\n Transition sustem has", len(Tp.get("Tp.Q")), "sub-polytopes;  \n\t time spent for creating"
                                                    " it (without disabling unfeasible transitions) :", str(stop - start), "secs")
start = os.times()[4]
Tp = invalidate_transitions.Invalid_Transition(Tp, U_A, U_b, D_A, D_B, D_b, A)
stop = os.times()[4]

print("\n Time spent for eliminating unfeasible tranisitions", str(start - stop), "secs \n")

if n == 2 or n == 3:
    init_fig = plt_tr_sys_polyt.PlotTransitionSystem(Tp, A, b)
    h_vf = plot_drift.PlotDrift(init_fig, D_A, D_b, A[-1], b[-1])

Alph_s = alphabet_set.Alphs_set(alphabet)

repeat = 'Y'
Use_mine = True

while repeat == 'Y' or repeat == 'y':

    formula = read_formula.Read_formula(alphabet, orig_alph)

    start = os.times()[4]
    B = create_buchi.CreateBuchi(formula, Alph_s)
    stop = os.times()[4]
    print("\n Buchi automaton has",str(len(B.get("B.S"))), "state; time spent for creating it :", str(start - stop))

    X0 = input("Enter Initial continuous state x0 (column vector) 2 x 1")
    if Use_mine:
        X0 = np.array([[-4], [1]])

    start = os.times()[4]
    Tp_Q0 = find_init_state.findInitState(A, B, X0, Tp.get("Tp.signs"),
                                          accepted_init_state.Accepted_Q0.accept_Q0)
    stop = os.times()[4]

    tmp_run_tp = [[[14, 1, 0], [2, 25, 22, 19, 22, 25, 2, 0]]]
    # accepted_init_state.Accepted_Q0.accept_run[Tp_Q0[0]]

    if len(Tp_Q0) == 0 or ismember(Tp_Q0, accepted_init_state.Accepted_Q0.accept_Q0):
        print("\n Wrong initial state")

    else:
        [ctrl, Speed] = control_sequence.control_sequence(Tp, U_A, U_b, D_A, D_B, D_b, tmp_run_tp)
        time_step = 0.01

        [t_ev, X, C, S] = simulate_system.simulatesystem(Tp, D_A, D_B, D_b, X0, tmp_run_tp, ctrl, time_step, 2)
        print(X)

        if n == 2 or n == 3:
            plot_run.plotrun(Tp, tmp_run_tp, h_vf)

            plot_trajectory.plottrajectory(h_vf, t_ev, X)

        repeat = input("Do you want to try another LTL formula? Y/N")


