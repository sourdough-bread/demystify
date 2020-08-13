#!/usr/bin/env python3
import copy
import sys
import os
import logging

# Let me import puzsmt from one directory up
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) 
import puzsmt
import puzsmt.base
import puzsmt.internal
import puzsmt.MUS
import puzsmt.solve
import puzsmt.prettyprint
import buildpuz

logging.basicConfig(level=logging.INFO)

# Make a matrix of variables (we can make more than one)
vars = puzsmt.base.VarMatrix(lambda t: (t[0]+1,t[1]+1), (9, 9), range(1,9+1))

# Build the puzzle (we can pass multiple matrices, depending on the puzzle)
puz = puzsmt.base.Puzzle([vars])


thermometers = [
    [(1,4),(0,3),(1,2),(2,3)],
    [(2,4),(1,3)],
    [(1,6),(2,5),(3,4)],
    [(2,6),(3,7),(4,6),(3,5)],
    [(5,6),(6,7),(7,6),(6,5),(5,4)],
    [(6,6),(7,5),(6,4),(5,5)]

]
puz.addConstraints(buildpuz.basicMiracle2(vars, thermometers))


solver = puzsmt.internal.Solver(puz)

sudoku = [ [None] * 9 for _ in range(9) ]
sudoku[1][3] = 9



# First, we turn it into an assignment (remember technically an assignment is a list of variables, so we pass [sudoku])

sudokumodel = puz.assignmentToModel([sudoku])

fullsolution = solver.solveSingle(sudokumodel)

# Then we 'add' all the assignments that we know (this is what we can undo later with a 'pop')
for s in sudokumodel:
    solver.addLit(s)

# The 'puzlits' are all the booleans we have to solve
# Start by finding the ones which are not part of the known values
puzlits = [p for p in fullsolution if p not in sudokumodel]

MUS = puzsmt.MUS.CascadeMUSFinder(solver)

trace = puzsmt.solve.html_solve(sys.stdout, solver, puzlits, MUS)
        
print("Trace: ", trace)
print("corecount: ", solver._corecount)