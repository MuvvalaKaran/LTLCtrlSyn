from read_data import ReadData
import numpy as np
import re

alphabet = ReadData.alphabet
orig_alph = ReadData.orig_alph

class Read_formula:
    N_p = len(alphabet) - 1
    formula = input("LTL_x (without next operator) formula (between apostrophes) involving all" + str(N_p) + "atomic propositions:\n")
    rev_Np = np.arange(N_p,-1,-1)
    for i in rev_Np:
        formula = re.sub(orig_alph[i],alphabet[i],formula)
    print(formula)

