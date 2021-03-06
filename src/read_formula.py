from src.read_data import  ReadData
import numpy as np
import re


class Read_formula:
    """
    A class that reads an LTL formula and replaces names of proposition
    """

    def __init__(self, alphabet, orig_alph):
        self.alphabet = alphabet
        self.orig_alph  = orig_alph

    def readformula(self):

        alphabet = self.alphabet
        orig_alph = self.orig_alph
        read_formula = True

        N_p = len(alphabet) - 1
        formula = input("LTL_x (without next operator) formula (between apostrophes) involving all " + str(N_p) + "atomic propositions:\n")
        if read_formula:
            formula = 'G(F((p3 & p10) & F((!p4 & p5 & p6 & p8) & F(!p1 & !p6 & p8))) & !(p4 | p7 |(p1 & !p2 & !p5 & p9)))'
        rev_Np = np.arange(N_p, - 1, -1)
        for i in rev_Np:
            formula = re.sub(orig_alph[i], alphabet[i], formula)
        if not read_formula:
            print(formula)

        return formula

