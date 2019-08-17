## the main class that will used to call things
import src.find_init_state as find_init_state
import src.read_data as read_data
import src.trans_sys_polytope as trans_sys_polyTope
import src.accepted_init_states as accepted_init_state
import src.control_sequence as control_sequence
import numpy as np

def ismember(a, b):
    for counter, i in enumerate(b):
        ret = False
        if a == i:
            # ret.append(counter)
            ret = True
            break
    return ret

Use_mine = True
X0 = input("Enter Initial continuous state x0 (column vector) 2 x 1")
if Use_mine:
    X0 = np.array([[-4], [1]])


Tp_Q0 = find_init_state.findInitState(read_data.ReadData.A, read_data.ReadData.B, X0,

                                      trans_sys_polyTope.TransSysToPolytope.Tp_Signs,
                                      accepted_init_state.Accepted_Q0.accept_Q0)

if len(Tp_Q0) == 0 or not ismember(Tp_Q0, accepted_init_state.Accepted_Q0.accept_Q0):
    print("\n Wrong initial state")

else:
    [ctrl , Speed] = control_sequence.control_sequence(trans_sys_polyTope.TransSysToPolytope.Tp)

