#!/usr/bin/env python3
import sys
import os
import logging

# Let me import demystify from one directory up
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import demystify
import demystify.base
import demystify.internal
import demystify.musocus
import demystify.musforqes
# import demystify.prettyprint
# import demystify.solve
import demystify.buildpuz

ncols_sudoku = 4

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s"
)

demystify.config.LoadConfigFromDict({"repeats": 5, "cores": 4})

# Make a matrix of variables (we can make more than one)
vars = demystify.base.VarMatrix(lambda t: (t[0] + 1, t[1] + 1), (ncols_sudoku, ncols_sudoku), range(1, ncols_sudoku + 1))

# Build the puzzle (we can pass multiple matrices, depending on the puzzle)
puz = demystify.base.Puzzle([vars])
puz.addConstraints(demystify.buildpuz.basicSudoku(vars))


solver = demystify.internal.Solver(puz)

# Now, let's get an actual Sudoku!
# str = "600120384008459072000006005000264030070080006940003000310000050089700000502000190"

if ncols_sudoku == 4:
    sudokustr = (
        "0340400210030210"
    )
else:
    sudokustr = (
        "093004560060003140004608309981345000347286951652070483406002890000400010029800034"
    )

l = [int(c) for c in sudokustr]
sudoku = [l[i : i + ncols_sudoku] for i in range(0, len(l), ncols_sudoku)]

print("Going to solve:")
print(sudoku)
# We need to put 'None' in places where we don't want a value (in case we want 0, we could hard-wire 0 = empty)

for i in range(ncols_sudoku):
    for j in range(ncols_sudoku):
        if sudoku[i][j] == 0:
            sudoku[i][j] = None

# First, we turn it into an assignment (remember technically an assignment is a list of variables, so we pass [sudoku])

sudokumodel = puz.assignmentToModel([sudoku])

fullsolution = solver.solveSingle(sudokumodel)
print(f"{fullsolution=}")

# print(f"{solver.__dir__()=}")
print(f"{solver._puzzle=}")
print(f"{solver._solver=}")
print(f"{solver._conlits=}")
print(f"{solver._varlit2smtmap=}")
print(f"{solver._varsmt2litmap=}")
print(f"{solver._varsmt2neglitmap=}")
print(f"{solver._varsmt=}")
print(f"{solver._knownlits=}")
print(f"{solver._cnf=}")
print(f"{solver._varlit2con=}")
print(f"{solver._varlit2negconnectedlits=}")
print(f"{solver._varlit2con2=}")

# Then we 'add' all the assignments that we know (this is what we can undo later with a 'pop')
for s in sudokumodel:
    solver.addLit(s)

# The 'puzlits' are all the booleans we have to solve
# Start by finding the ones which are not part of the known values
puzlits = [p for p in fullsolution if p not in sudokumodel]

# MUS = demystify.musforqes.ForqesMUSFinder(solver)
# TODO: 1.Get the things working:
# TODO: 1.1 How to get the CNF
# TODO: 1.2 How to get the assumptions ?
# TODO: 1.3 Link with pyexplain
# TODO: 1.4 SETUP: hs solver - link with gurobi
# TODO: 1.5 Single Step explain call
# TODO: 1.6 Basic sudoku explanations running
# TODO: 2. Pretty printing and cleaning of the explanations
# TODO: 3. Improving the explanations
# TODO: 3.1 Adding different weights
# TODO: 3.2 Adding extra constraints if necessary
# TODO: 4. HTML_Solve?

# MUS = demystify.musocus.OCUSMUSFinder(solver)


# trace = demystify.solve.html_solve(sys.stdout, solver, puzlits, MUS)


# print("Minitrace: ", [(s, mins[0], len(mins)) for (s, mins) in trace])


# logging.info("Finished")
# logging.info("Full Trace %s", trace)
