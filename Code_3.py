## parsa badiei

import math
import random

grid=0
gridPath=0
policyEvaluationGrid=0
PEGTemp=0
xGoal=8
yGoal=4
def main():

    initGrid()
    iteratePolicy()
    return

def initGrid():
    global grid
    grid = [[' ' for x in range(9)] for y in range(9)]
    grid[0][0] = '*'
    grid[0][1] = '*'
    grid[0][2] = '*'
    grid[0][7] = '*'
    grid[0][8] = '*'

    grid[1][5] = 'X'
    grid[1][8] = '*'

    grid[2][1] = 'X'
    grid[2][2] = 'X'
    grid[2][3] = 'X'
    grid[2][4] = 'X'
    grid[2][5] = 'X'
    grid[2][6] = 'X'

    grid[3][3] = '*'
    grid[3][4] = '*'
    grid[3][5] = '*'
    grid[3][7] = 'X'

    grid[4][2] = 'X'
    grid[4][3] = 'X'
    grid[4][4] = 'X'
    grid[4][5] = 'X'
    grid[4][6] = 'X'
    grid[yGoal][xGoal] = 'G'

    grid[5][7] = 'X'

    grid[6][1] = 'X'
    grid[6][2] = 'X'
    grid[6][3] = 'X'
    grid[6][4] = 'X'
    grid[6][5] = 'X'
    grid[6][6] = 'X'

    for i in range(1,7):
        grid[7][i] = '*'

    grid[7][8] = 'X'
    grid[8][8] = 'X'

    for i in range(1,7):
        grid[8][i] = '*'
    grid[8][4]='X'


    #for the path grid
    global gridPath
    gridPath = [['' for x in range(9)] for y in range(9)]
    gridPath[yGoal][xGoal]= 'G'
    #for the policyEvaluationGrid
    global policyEvaluationGrid
    policyEvaluationGrid = [[0 for x in range(9)] for y in range(9)]
    #for the temporary policeevaluationgrid
    global PEGTemp
    PEGTemp = [[0 for x in range(9)] for y in range(9)]
    return

def produceAction():

    p = random.random()
    if(p<0.5):
        return 'r'
    else:
        p2 = random.randint(0,3)
        action= {
            0 : 'r',
            1 : 'l',
            2 : 'u',
            3 : 'd'
        }

    return action[p2]

def applyAction(xs,ys,a):
    state = {
        '*':  5,
        'X': -20,
        ' ': -1,
        'G': 100
    }
    if(grid[ys][xs]=='G'):
        return state[grid[ys][xs]],xs,ys

    offgrid = False
    xsTemp = xs
    ysTemp = ys
    reward=0
    if (a=='r'):
        xsTemp = xs + 1
    elif (a == 'l'):
        xsTemp = xs - 1
    elif (a == 'u'):
        ysTemp = ys - 1
    elif (a == 'd'):
        ysTemp = ys + 1
    elif(a=='rd'):
        ysTemp=ys+1
        xsTemp=xs+1
    elif (a == 'ru'):
        ysTemp = ys - 1
        xsTemp = xs + 1
    elif (a == 'ld'):
        ysTemp = ys + 1
        xsTemp = xs - 1
    elif (a == 'lu'):
        ysTemp = ys - 1
        xsTemp = xs - 1

    if (xsTemp == -1 or xsTemp==9):
        xsTemp = xs
        reward = -10
        offgrid = True
    if (ysTemp == -1 or ysTemp==9):
        ysTemp = ys
        reward = -10
        offgrid = True

    if(offgrid):
        return reward,xsTemp,ysTemp
    if(grid[ysTemp][xsTemp] == 'X'):
        return  -20,xs,ys
    return state[grid[ysTemp][xsTemp]],xsTemp,ysTemp

def iteratePolicy():
    global gridPath
    global policyEvaluationGrid
    global PEGTemp
    randomPolicy = [i for i in range(81)]
    GoalIsReached = True
    landa = 1
    discountRate = 0.8
    sweepcount=1
    while GoalIsReached:
        expectedValue=0
        delta=0
        # reward = 0
        # reward_sum = 0
        #coordinate for the resulting states, to calculate expected value
        xsR , ysR , xsL, ysL , xsU, ysU, xsD, ysD = 0 ,0,0,0,0,0,0,0
        xsRu, ysRu, xsLu, ysLu, xsrd, ysrd, xsld, ysld = 0, 0, 0, 0, 0, 0, 0, 0
        rewardR, rewardL, rewardU, rewardD = 0,0,0,0
        rewardRU, rewardLU, rewardRD, rewarLD = 0, 0, 0, 0

        #do a sweep for every cell
        for i in range(81):
            ys = int(i / 9)
            xs = i % 9
            #calculate the expected value, starting from xs and ys
            rewardR, xsR, ysR = applyAction(xs,ys,'r')
            rewardL, xsL, ysL = applyAction(xs, ys, 'l')
            rewardU, xsU, ysU = applyAction(xs, ys, 'u')
            rewardD, xsD, ysD = applyAction(xs, ys, 'd')
            rewardRU, xsRu, ysRu = applyAction(xs, ys, 'ru')
            rewardLU, xsLu, ysLu = applyAction(xs, ys, 'lu')
            rewardRD, xsrd, ysrd = applyAction(xs, ys, 'rd')
            rewardLD, xsld, ysld = applyAction(xs, ys, 'ld')
## for this part we will calculate the probability of each direction
            expectedValue = 0.361*(rewardR + policyEvaluationGrid[ysR][xsR])\
                            +0.062*(rewardL + policyEvaluationGrid[ysL][xsL])\
                            +0.062*(rewardD + policyEvaluationGrid[ysD][xsD])\
                            +0.062*(rewardU + policyEvaluationGrid[ysU][xsU])\
                            +0.161*(rewardRU + policyEvaluationGrid[ysRu][xsRu])\
                            +0.062*(rewardLU + policyEvaluationGrid[ysLu][xsLu])\
                            +0.161*(rewardRD + policyEvaluationGrid[ysrd][xsrd])\
                            +0.062*(rewardLD + policyEvaluationGrid[ysld][xsld])
## for example direction Right: 0.6 * 0.562 + 0.2 * 0.062 + 0.2 * 0.062 = 0.337 + 0.012 + 0.012 = 0.361
            PEGTemp[ys][xs] = round(expectedValue*landa,1)
            delta = max(delta,abs(policyEvaluationGrid[ys][xs]-PEGTemp[ys][xs]))
            #path.append((xs,ys))


        #update the expected values
        policyEvaluationGrid = PEGTemp
        policyEvaluationGrid[yGoal][xGoal] = 100
        # increase Landa
        landa *= discountRate
        #check for the termination rules
        #(or delta<0.01 or
        if( (xs==xGoal and ys==yGoal) or landa<0.05 ):
            GoalIsReached = False
        print("========================= sweep=", sweepcount)
        for y in range(9):
            print(policyEvaluationGrid[y])
        print("greedy policy")
        printGreedy()
        sweepcount+=1

    return

def printGreedy():
    for i in range(9):
        gridPath[i]=['']*9

    for i in range(81):
        ys = int(i / 9)
        xs = i % 9

        if (xs == 8 and ys == 0):
            maxNeighbour = max(policyEvaluationGrid[0][7], policyEvaluationGrid[1][8], policyEvaluationGrid[1][7])
            if (maxNeighbour == policyEvaluationGrid[0][7]):
                gridPath[ys][xs] += '←'
            if (maxNeighbour == policyEvaluationGrid[1][8]):
                gridPath[ys][xs] += '↓'
            if (maxNeighbour == policyEvaluationGrid[1][7]):
                gridPath[ys][xs] += '⸝'
            continue

        if(xs==0 and ys==0):
            maxNeighbour = max(policyEvaluationGrid[0][1], policyEvaluationGrid[1][0], policyEvaluationGrid[1][1])
            if (maxNeighbour == policyEvaluationGrid[0][1]):
                gridPath[ys][xs] += '→'
            if (maxNeighbour == policyEvaluationGrid[1][0]):
                gridPath[ys][xs] +='↓'
            if (maxNeighbour == policyEvaluationGrid[1][1]):
                gridPath[ys][xs] += '⸜'
            continue
        if(xs==0 and ys==8):
            maxNeighbour = max(policyEvaluationGrid[8][1], policyEvaluationGrid[7][0], policyEvaluationGrid[7][1])
            if (maxNeighbour == policyEvaluationGrid[8][1]):
                gridPath[ys][xs] = '→'
            if (maxNeighbour == policyEvaluationGrid[7][0]):
                gridPath[ys][xs] = '↑'
            if (maxNeighbour == policyEvaluationGrid[7][1]):
                gridPath[ys][xs] = '⸍'
            continue
        if(xs==8 and ys==8):
            maxNeighbour = max(policyEvaluationGrid[8][7], policyEvaluationGrid[7][8], policyEvaluationGrid[7][7])
            if (maxNeighbour == policyEvaluationGrid[8][7]):
                gridPath[ys][xs] = '←'
            if (maxNeighbour == policyEvaluationGrid[7][8]):
                gridPath[ys][xs] = '↑'
            if (maxNeighbour == policyEvaluationGrid[7][7]):
                gridPath[ys][xs] = '⸌'
            continue

        if(xs==0):
            maxNeighbour = max(policyEvaluationGrid[ys][xs + 1], policyEvaluationGrid[ys - 1][xs],
                               policyEvaluationGrid[ys + 1][xs], policyEvaluationGrid[ys + 1][xs + 1],
                               policyEvaluationGrid[ys - 1][xs + 1])
            if (maxNeighbour == policyEvaluationGrid[ys][xs + 1]):
                gridPath[ys][xs] += '→'
            if (maxNeighbour == policyEvaluationGrid[ys - 1][xs]):
                gridPath[ys][xs] += '↑'
            if (maxNeighbour == policyEvaluationGrid[ys + 1][xs]):
                gridPath[ys][xs] += '↓'
            if (maxNeighbour == policyEvaluationGrid[ys + 1][xs + 1]):
                    gridPath[ys][xs] += '⸜'
            if (maxNeighbour == policyEvaluationGrid[ys - 1][xs + 1]):
                        gridPath[ys][xs] += '⸍'
            continue

        if(xs == 8):
            maxNeighbour = max(policyEvaluationGrid[ys][xs - 1], policyEvaluationGrid[ys - 1][xs],
                               policyEvaluationGrid[ys + 1][xs], policyEvaluationGrid[ys + 1][xs - 1],
                               policyEvaluationGrid[ys - 1][xs - 1])
            if (maxNeighbour == policyEvaluationGrid[ys][xs - 1]):
                gridPath[ys][xs] += '←'
            if (maxNeighbour == policyEvaluationGrid[ys - 1][xs]):
                gridPath[ys][xs] += '↑'
            if (maxNeighbour == policyEvaluationGrid[ys + 1][xs]):
                gridPath[ys][xs] += '↓'
            if (maxNeighbour == policyEvaluationGrid[ys + 1][xs - 1]):
                gridPath[ys][xs] += '⸝'
            if (maxNeighbour == policyEvaluationGrid[ys - 1][xs - 1]):
                gridPath[ys][xs] += '⸌'
            continue

        if(ys == 0):
            maxNeighbour = max(policyEvaluationGrid[ys][xs - 1], policyEvaluationGrid[ys][xs + 1],
                               policyEvaluationGrid[ys + 1][xs], policyEvaluationGrid[ys + 1][xs - 1],
                               policyEvaluationGrid[ys + 1][xs + 1])
            if (maxNeighbour == policyEvaluationGrid[ys][xs - 1]):
                gridPath[ys][xs] += '←'
            if (maxNeighbour == policyEvaluationGrid[ys][xs + 1]):
                gridPath[ys][xs] += '→'
            if (maxNeighbour == policyEvaluationGrid[ys + 1][xs]):
                gridPath[ys][xs] += '↓'
            if (maxNeighbour == policyEvaluationGrid[ys + 1][xs - 1]):
                gridPath[ys][xs] += '⸝'
            if (maxNeighbour == policyEvaluationGrid[ys + 1][xs] + 1):
                gridPath[ys][xs] += '⸜'
            continue

        if(ys == 8):
            maxNeighbour = max(policyEvaluationGrid[ys][xs - 1], policyEvaluationGrid[ys][xs + 1],
                               policyEvaluationGrid[ys - 1][xs], policyEvaluationGrid[ys - 1][xs - 1],
                               policyEvaluationGrid[ys - 1][xs + 1])
            if (maxNeighbour == policyEvaluationGrid[ys][xs - 1]):
                gridPath[ys][xs] += '←'
            if (maxNeighbour == policyEvaluationGrid[ys][xs + 1]):
                gridPath[ys][xs] += '→'
            if (maxNeighbour == policyEvaluationGrid[ys - 1][xs]):
                gridPath[ys][xs] += '↑'
            if (maxNeighbour == policyEvaluationGrid[ys - 1][xs - 1]):
                gridPath[ys][xs] += '⸌'
            if (maxNeighbour == policyEvaluationGrid[ys - 1][xs + 1]):
                gridPath[ys][xs] += '⸍'
            continue

        else:
            maxNeighbour = max(policyEvaluationGrid[ys][xs-1],policyEvaluationGrid[ys][xs+1],
                               policyEvaluationGrid[ys-1][xs],policyEvaluationGrid[ys+1][xs],
                               policyEvaluationGrid[ys - 1][xs - 1], policyEvaluationGrid[ys + 1][xs - 1],
                               policyEvaluationGrid[ys - 1][xs + 1], policyEvaluationGrid[ys + 1][xs + 1])
            if(maxNeighbour == policyEvaluationGrid[ys][xs-1] ):
                gridPath[ys][xs] +='←'
            if(maxNeighbour == policyEvaluationGrid[ys][xs+1]):
                gridPath[ys][xs] += '→'
            if ( maxNeighbour == policyEvaluationGrid[ys-1][xs]):
                gridPath[ys][xs] += '↑'
            if(maxNeighbour == policyEvaluationGrid[ys+1][xs]):
                gridPath[ys][xs] += '↓'
            if (maxNeighbour == policyEvaluationGrid[ys - 1][xs - 1]):
                gridPath[ys][xs] += '⸝'
            if (maxNeighbour == policyEvaluationGrid[ys + 1][xs - 1]):
                gridPath[ys][xs] += '⸌'
            if (maxNeighbour == policyEvaluationGrid[ys - 1][xs + 1]):
                gridPath[ys][xs] += '⸍'
            if (maxNeighbour == policyEvaluationGrid[ys + 1][xs + 1]):
                gridPath[ys][xs] += '⸜'


    #  ← ↑ → ↓  ⸌ ⸍ ⸜ ⸝
    for i in range(9):
        print(gridPath[i])
    return

main()
