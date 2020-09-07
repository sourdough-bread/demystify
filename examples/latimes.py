#!/usr/bin/env python3
import copy
import sys
import os
import logging
import argparse
import json

# Let me import demystify from one directory up
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import demystify
import demystify.base
import demystify.internal
import demystify.MUS
import demystify.solve
import demystify.prettyprint
import buildpuz


parser = argparse.ArgumentParser()

parser.add_argument("sudoku", help="which latimes sudoku to use", type=int)
parser.add_argument("config", help="solver config", type=str)
args = parser.parse_args()

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s:%(name)s:%(relativeCreated)d:%(message)s"
)

demystify.config.LoadConfigFromDict({"cores": 16, "smallRepeats": 1, "repeats": 100, "solver": "cadical", "solveLimited": False})
demystify.config.LoadConfigFromDict(json.loads(args.config))

# Make a matrix of variables (we can make more than one)
vars = demystify.base.VarMatrix(lambda t: (t[0] + 1, t[1] + 1), (9, 9), range(1, 9 + 1))

# Build the puzzle (we can pass multiple matrices, depending on the puzzle)
puz = demystify.base.Puzzle([vars])
puz.addConstraints(buildpuz.basicSudoku(vars))


solver = demystify.internal.Solver(puz)

gridtypes= [ 
    ([# Diabolical - 4 Sep 2020
    "007010600",
    "000537000",
    "020004010",
    "012000000",
    "800000004",
    "003000250",
    "060700030",
    "000498000",
    "004620900"
    ], None),
    ([# Tough - 3 Sep 2020
    "000000034",
    "007860000",
    "100030008",
    "008009720",
    "000000000",
    "016200900",
    "400090006",
    "000074210",
    "000000000"
    ], None),
    ([# Tough - 30 Aug 2020
    "000567000",
    "080000000",
    "090408501",
    "470000002",
    "009000800",
    "600000039",
    "804302075",
    "000000060",
    "000970000"
    ],[((2,1),1),((2,1),2),((2,3),1),((2,3),2),((4,7),1)] ),
    ([# Diabolical - 28 Aug 2020
    "500009006",
    "300108000",
    "604000020",
    "008900500",
    "050000030",
    "001004900",
    "000000705",
    "000802004",
    "000700003"
    ],[((1,2),2),((1,3),2),((3,4),3)] ),
    ([# Tough - 27 Aug 2020
    "000094060",
    "710502000",
    "000000020",
    "108000352",
    "200000008",
    "945000706",
    "020000000",
    "000705031",
    "070480000"
    ],[((2,3),3)]  ),
    ([# Tough - 23 Aug 2020
    "300700400",
    "080003910",
    "000000000",
    "950070004",
    "400001006",
    "000060023",
    "000000000",
    "020507030",
    "008004009"
    ],[((7,5),1),((7,7),8)] ),
    ([#Diaboloical - 21 Aug 2020
    "070003060",
    "000102000",
    "005000709",
    "007200001",
    "006010840",
    "800000500",
    "704000900",
    "000708000",
    "090600050"
    ],[((8,7),3), ((5,9),3), ((6,2),3), ((6,3),3), ((9,5),3)]  ),
    ([ # Tough Thu, 20-Aug-2020
    "850020000",
    "020000003",
    "009108000",
    "040080150",
    "090010020",
    "083060070",
    "000605800",
    "200000030",
    "000090047"
    ], [((3,5),3)] ),
    ([# Tough - 16 Aug 2020
    "700000205",
    "000050001",
    "009003400",
    "000590100",
    "900214006",
    "001087000",
    "006100300",
    "800060000",
    "007000002"
    ], None),
    ([# Diabolical - 14 Aug 2020
    "020000005",
    "400905200",
    "005070090",
    "500107000",
    "003000800",
    "000504000",
    "010020000",
    "009700003",
    "600000079"
    ], None),
    ([# Tough - 13 Aug 2020
    "090060028",
    "000000000",
    "507000409",
    "400530000",
    "082000630",
    "000082004",
    "005000301",
    "000090000",
    "130040000"
    ], None),
    ([# Tough - 9 Aug 2020
    "000500000",
    "005400001",
    "000002098",
    "960000012",
    "040000060",
    "030000009",
    "780200005",
    "300081200",
    "000009000"
    ], None),
    ([# Diabolical - 7 Aug 2020
    "008007400",
    "070000003",
    "005301609",
    "050106000",
    "000050000",
    "000804090",
    "409608100",
    "600000030",
    "007400800"
    ], None),
    ([# Tough - 6 Aug 2020
    "501006090",
    "000400006",
    "060103000",
    "900030700",
    "200090003",
    "004010002",
    "000907030",
    "400002000",
    "020300409"
    ], None),
    ([# Tough - 2 Aug 2020
    "572000080",
    "030400000",
    "040200000",
    "000040030",
    "700903001",
    "310080007",
    "000005040",
    "000009070",
    "090000812"
    ], None),
    ([# Diabolical - 31 July 2020
    "807019030",
    "006070000",
    "050000007",
    "001000020",
    "700801005",
    "020030900",
    "900000080",
    "000060400",
    "000280700"
    ], None),
    ([# Tough - 30 July 2020
    "000000095",
    "103070608",
    "000050700",
    "900000400",
    "030107050",
    "004005007",
    "001060000",
    "508020304",
    "290000000"
    ], None),
    ([# Tough - 26 July 2020
    "007084000",
    "180000004",
    "002000903",
    "800200001",
    "000916000",
    "200008007",
    "501000800",
    "600000012",
    "000420700"
    ], None),
    ([# Diabolical - 24 Jul 2020 
    "400602000",
    "090000003",
    "700004060",
    "040010000",
    "063000159",
    "000020030",
    "080100006",
    "950000080",
    "000300005"
    ], None),
    ([# Tough - 23 Jul 2020
    "000050008",
    "000300006",
    "004910000",
    "803000600",
    "700000001",
    "009000702",
    "000093260",
    "400008000",
    "600071003"
    ], None),
    ([# Tough 19 Jul 2020 
    "080000019",
    "001000300",
    "050043000",
    "005470600",
    "090010050",
    "004038000",
    "000320000",
    "009000100",
    "720000060"
    ], None),
    ([# Diabolical - 17 Jul 2020
    "010006050",
    "300000000",
    "678900204",
    "000400007",
    "004010600",
    "700003000",
    "809005172",
    "000000009",
    "040200080"
    ], None),
    ([# Tough - 16 Jul 2020
    "020007060",
    "030000790",
    "007692000",
    "004000800",
    "810000075",
    "006000000",
    "000764900",
    "043000020",
    "060500040"   
    ], None),
    ([# Tough - 12 Jul 2020
    "008000001",
    "090000200",
    "000030904",
    "100800005",
    "080600020",
    "300405007",
    "704960000",
    "006000070",
    "900000400"
    ], None),
    ([# Diabolical - 10 Jul 2020
    "080270460",
    "100400005",
    "000000007",
    "600000090",
    "000603000",
    "030000072",
    "400000000",
    "200307009",
    "069042080"    
    ], None)
]

tooeasygrids = [
        [ # Moderate Wed 19-Aug-2020
    "040000120",
    "300107000",
    "080000073",
    "200001700",
    "900402001",
    "008900006",
    "820000010",
    "000703008",
    "093000050",
    ],
    [ # Gentle Tue 18-Aug-2020
    "100080009",
    "000000863",
    "000300017",
    "003400200",
    "000825000",
    "005009600",
    "980003000",
    "376000000",
    "200090001"
    ]
]

(grid, moves) = gridtypes[args.sudoku]

if moves is not None:
    lits = [demystify.base.NeqVal(vars[x-1][y-1], d) for ((x,y),d) in moves]
else:
    lits = None

sudoku = [[None] * 9 for _ in range(9)]
for i in range(9):
    for j in range(9):
        if grid[i][j] != '0':
            sudoku[i][j] = int(grid[i][j])

# First, we turn it into an assignment (remember technically an assignment is a list of variables, so we pass [sudoku])

sudokumodel = puz.assignmentToModel([sudoku])

fullsolution = solver.solveSingle(sudokumodel)

# Then we 'add' all the assignments that we know (this is what we can undo later with a 'pop')
for s in sudokumodel:
    solver.addLit(s)

# The 'puzlits' are all the booleans we have to solve
# Start by finding the ones which are not part of the known values
puzlits = [p for p in fullsolution if p not in sudokumodel]

MUS = demystify.MUS.CascadeMUSFinder(solver)

trace = demystify.solve.html_solve(sys.stdout, solver, puzlits, MUS, forcechoices = lits)

print("Minitrace: ", [(s, mins[0], len(mins)) for (s, mins) in trace])


logging.info("Finished")
logging.info("Full Trace %s", trace)
