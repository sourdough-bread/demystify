import math
import logging
import sys
import math
# from pyexplain import OCUSExplain

class OCUSMUSFinder:
    def __init__(self, solver, weights=None, user_vars=None):
        self._solver = solver
        self._bestcache = {}

        # Internals for OCUS
        p_clauses = solver._cnf
        p_ass = [[c] for c in solver._conlits]

        if weights is not None:
            p_weights = weights
        else:
            # Demystify has no weighting so weight everything equally.
            p_weights = {c: 20 for c in solver._conlits}

        if user_vars is not None:
            p_user_vars = solver._varsmt
        else:
            p_user_vars = user_vars

        # print("n_clauses=", len(p_clauses))
        # print("n_ass=", len(p_ass))
        # print("n_ass=", p_ass[:10])
        # print("n_ass=", p_ass[1000:1010])
        # print("n__user_vars=", len(p_user_vars))
        # print(f"{p_clauses=}")
        # print(f"{p_ass=}")
        # print(f"{p_weights=}")
        # print(f"{p_user_vars=}")

    def smallestMUS(self, puzlits):
        pass
        # TO DO
