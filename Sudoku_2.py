from math import *
from random import *
from time import *

SIZE = 9
subSIZE = int(sqrt(SIZE))
alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alpha = alpha[:SIZE]
nums = "123456789"
blank = "."
#############################################
squares = [a+n for a in alpha for n in nums]
units = []
units.extend([[alpha[x]+n for n in nums] for x in range(SIZE)])    # 9 rows
units.extend([[a+nums[x] for a in alpha] for x in range(SIZE)])    # 9 cols
for x in range(0,SIZE,subSIZE):  # 9 subsquares
    alphaRange = alpha[x:x+subSIZE]
    for y in range(0,SIZE,subSIZE):
        numRange = nums[y:y+subSIZE]
        units.append([a + n for a in alphaRange for n in numRange])
peers = {}
rows, cols, subs = units[:SIZE], units[SIZE:SIZE*2], units[SIZE*2:]
for p in squares:   # peers dictionary -- {square : set(all surrounding)}
    temp = set()
    rowInd, colInd = alpha.index(p[0]), nums.index(p[1])
    for x in range(SIZE):
        if p in subs[x]:    break
    subInd = x
    temp.update([r for r in rows[rowInd] if r != p])
    temp.update([c for c in cols[colInd] if c != p])
    temp.update([s for s in subs[subInd] if s != p])
    peers[p] = temp
########################################################################################################
def gridForm(board):
    state, bool = board
    grid = ""
    rCt = 0
    for r in rows:
        if rCt % 3 == 0:    grid += "-" * 25 + "\n"
        sqCt = 0
        for sq in r:
            if sqCt%3==0: grid+="| "
            if bool[sq] == True:    grid+=state[sq]+" "
            else:   grid+=". "
            sqCt+=1
        grid+="|"
        grid+="\n"
        rCt+=1
    grid += "-" * 25 + "\n"
    return grid
def init(str):
    state = dict(zip(squares, [nums if x == blank else x for x in str]))
    bool = dict(zip(squares, [False if x == blank else True for x in str]))
    for s in [x for x in squares if bool[x] == False]:  # for all squares not assigned, update to remove conflicts w other vars already assigned
        peerVals = set(state[x] for x in peers[s] if bool[x] == True) # all vals that blanks CANNOT be
        state[s] = "".join([x for x in state[s] if x not in peerVals])
    return (state, bool)
def goal_test(board):
    return False not in board[1].values()   # every position has been assigned smth
def consistent_test(board):
    return "" not in board[0].values()
def get_vals(board, var):
    return board[0][var]
def get_next_var(board):
    state, bool = board
    weighted = [(len(state[k]), randint(0, 10), k) for k in state.keys() if bool[k] == False]  # sorts cols w/o queen by set length and proximity to center
    weighted.sort()
    return weighted[0][2]
def assign(board, var, val):
    state, bool  = board
    newState, newBool = state.copy(), bool.copy()
    newState[var], newBool[var] = val, True  # assign square with value and mark it off
    # Update all peers
    varPeers = set(p for p in peers[var] if newBool[p] == False)  # unassigned peers
    for v in varPeers:
        if val in newState[v]:
            newState[v] = newState[v].replace(val, "")
            if len(newState[v]) == 1:
                (newState, newBool) = assign((newState, newBool), v, newState[v])
    return (newState, newBool)
def CSP(board):
    global numNodes
    numNodes += 1
    if goal_test(board):    return board
    var = get_next_var(board)
    for val in get_vals(board, var):
        newState = assign(board, var, val)
        if consistent_test(newState):
            result = CSP(newState)
            if result != False:
                return result
    return False
########################################################################################################
global numNodes
infile = open("sudoku_sample_puzzles.txt", "r")
for line in infile:
    numNodes = 0
    commaInd = line.index(",")
    board = init(line[commaInd+1:])
    tic = time()
    csp = CSP(board)
    toc = time()
    print(line[:commaInd], numNodes, toc - tic)
    print(gridForm(csp))

# str = ".32.....58..3.....9.428...1...4...39...6...5.....1.....2...67.8.....4....95....6."
# print(str)
# board = init(str)
# csp = CSP(board)
# print(gridForm(csp))
# print("Nodes:", numNodes)
# for key in board[0].keys():
#     print(key, board[0][key], board[1][key])

# ADDITIONAL CHECK: INSTEAD OF CHECKING SOLELY FOR SMALLEST POSSIBLE FOR VAR, ALSO CHECK IF THERE'S VALS WHERE ONLY GO IN ONE SQUARE