
import random


SIZE = 10
NUM_TURNS = 13
STUDENT = "S"
WORK = "w"
FUN = "f"
TAMINATOR = "T"
EMPTY = " "
debugOn = False
PAVEL_CHANCE = 9
MIN_P = 0
MAX_P = 9
MIN_T = 0
MAX_T = 3
P_CHANCE = 0
T_CHANCE = 1


def display(world):
    for r in range (0, SIZE, 1):
    # Row of dashes before each row

        for i in range (0, SIZE, 1):
            print(" -", end="")
        print()
        for c in range (0, SIZE, 1):
            # Vertical bar before displaying each element
            print("|" + world[r][c], end="")
        print("|") # Vertical bar right of last element + CR to
                           # move output to the next line

    # A line of dashes before each row, one line after the last
    # row.
    for i in range (0, SIZE, 1):
        print(" -", end="")
    print()



def initialize():
    world = []
    for r in range (0, SIZE, 1):
        world.append ([])
        for c in range (0, SIZE, 1):
            world[r].append ("!")
    return(world)


def readFromFile():
    r = -1
    c = -1
    world = initialize() # Needed to create the 2D list
    inputFilename = input("Name of input file: ")

    try:
        inputFile = open(inputFilename,"r")
        r = 0
        # Read one line at a time from the file into a string
        for line in inputFile:
            c = 0
            # Iterate 1 char at a time through the string
            for ch in line:
                # Including EOL there's 11 characters per line
                # 10x10 list , exclude the EOL to avoid reading
                # outside the bounds of the list (10 columns)
                if (c < SIZE):
                    # Set list element to the single char
                    # read from file
                    world[r][c] = ch
                    # Advance to next element along row
                    c = c + 1
                # Entire row has been set to values read in from
                # file, move to next row
            r = r + 1
        inputFile.close()
    except IOError:
        print("Error reading from " + inputFilename)
    return(world)




def studentPosition(world):
    for r in range (0, SIZE, 1):
        for c in range (0, SIZE, 1):
            if (world[r][c] == STUDENT):
                rSPosition = r
                cSPosition = c
    return(rSPosition, cSPosition)


# Movement display
def movementDisplay():
    print("""Movement options:
1 2 3
4 5 6
7 8 9
Type a number on the keypad to indicate direction of movement
Type 5 to pass on movement""")
    selection = input("Your selection: ")
    rangeSelection = ["1","2","3","4","5","6","7","8","9","0"]
    while (selection not in rangeSelection):
        print("""--------------------------------------------------
ERROR: your selection in not in range.
Movement options:
1 2 3
4 5 6
7 8 9
Type a number on the keypad to indicate direction of movement
Type 5 to pass on movement""")
        selection = input("Your selection: ")

    return(selection)


def movement(selection, world, rSPosition, cSPosition, funPoints, gpa, turn, turnMode, taminatorMode):
    upMovement= ["1","2","3"]
    downMovement= ["7","8","9"]
    leftMovement= ["1","4","7"]
    rightMovement= ["3","6","9"]
    zero = ["0"]

    world[rSPosition][cSPosition]= EMPTY
    if (selection in upMovement):
        if (rSPosition == 1):
            print("ERROR: You cannot go furthure up")
            turn = turn - 1
        else:
            rSPosition = rSPosition - 1

    elif (selection in downMovement):
        if (rSPosition == SIZE-1):
            print("ERROR: You cannot go furthure down")
            turn = turn-1
        else:
            rSPosition = rSPosition + 1

    if (selection in rightMovement):
        if (cSPosition == SIZE-1):
            print("ERROR: You cannot go furthure right")
            turn = turn-1
        else:
            cSPosition = cSPosition + 1

    elif (selection in leftMovement):
        if (cSPosition == 0):
            print("ERROR: You cannot go furthure left")
            turn = turn-1
        else:
            cSPosition = cSPosition - 1

    if (selection in zero):
        rTPosition, cTPosition, taminatorMode = cheatMenu(world, selection, turn, taminatorMode)
        print("*****************", taminatorMode, "********")
    if (taminatorMode == True):
        for r in range(0, SIZE, 1):
            for c in range(0, SIZE, 1):
                if (world[r][c] == TAMINATOR):
                    rTPosition = r
                    cTPosition = c
    if (taminatorMode == False):
        rTPosition = -1
        cTPosition = -1
    if (world[rSPosition][cSPosition] != EMPTY):
        funPoints, gpa = points(world, rSPosition, cSPosition, funPoints, gpa)

    world[rSPosition][cSPosition]= STUDENT
    turn = turn + 1
    print("----------------------------------------------")
    turnMode = turnPoints(turn, turnMode, funPoints, gpa)
#    display(world)
    return(world, rSPosition, cSPosition, turn, turnMode, funPoints, gpa, taminatorMode, rTPosition, cTPosition)




def turnPoints(turn, turnMode, funPoints, gpa):
    if (turn < 14):
        turnMode = True
        print("Current turn: ", turn)
        print("Fun points: ", funPoints, "     GPA: ", gpa)
    else:
        turnMode = False
    return(turnMode)


def points(world, rSPosition, cSPosition, funPoints, gpa):
    if (world[rSPosition][cSPosition] == FUN):
        funPoints = funPoints + 1
    elif (world[rSPosition][cSPosition] == WORK):
        gpa = gpa + 1
    return(funPoints, gpa)


def cheatMenu(world, selection, turn, taminatorMode):
    toggle = "t"
    make = "m"
    quitCh = "q"
    print("""Cheat Menu Options:
    (t)oggle debug mode on
    (m)ake the Taminator appear
    (q)uit cheat menu""")

    chSelection = input("Cheat menu selection: ")
    
    if (chSelection == toggle):
        debugOn = True
    elif (chSelection == make):
        print("Where do you want to put the Taminator?")
        rTPosition = int(input("Row: "))
        cTPosition = int(input("Column: "))
        #print("1111111111111111111 ", rTPosition, "******", cTPosition)
        while (world[rTPosition][cTPosition] != EMPTY):
            print("ERROR: The position you picked is occupied, Please choose another position.")
            rTPosition = int(input("Row: "))
            cTPosition = int(input("Column: "))
        taminatorMode = taminatorEvent(world, rTPosition, cTPosition, taminatorMode)
        display(world)
    elif (chSelection == quitCh):
        movementDisplay()
    return(rTPosition, cTPosition, taminatorMode)

def taminatorEvent(world, rTPosition, cTPosition, taminatorMode):
    print("<<< Beware! The Taminator is here!>>>")
    world[rTPosition][cTPosition] = TAMINATOR
    #print("222222222222222222", rTPosition, "******", cTPosition)
    taminatorMode = True
    return(taminatorMode)

def taminatorMovement(world, rTPosition, cTPosition, turn, rSPosition, cSPosition):
    lossTurn = False
    workPlace = False
    funPlace = False
    world[rTPosition][cTPosition] = EMPTY
    #print("33333333333333333333 ", rTPosition, "******", cTPosition)

    rTPattern = rTPosition - rSPosition
    cTPattern = cTPosition - cSPosition
    print("rTPattern= ", rTPattern, cTPattern)
    if (rTPattern > 2):
        rTPosition = rTPosition - 2
        #print("888888888888888888888888888888888888888888888888")
    elif (rTPattern < -2):
        rTPosition = rTPosition + 2
    elif (rTPattern == 2):
        rTPosition = rTPosition - 1
    elif (rTPattern == -2):
        rTPosition = rTPosition + 1
    if (cTPattern > 2):
        cTPosition = cTPosition - 2
    elif (cTPattern < -2):
        cTPosition = cTPosition + 2
    elif (cTPattern == 2):
        cTPosition = cTPosition - 1
    elif (cTPattern == -2):
        cTPosition = cTPosition + 1
    rTPattern = rTPosition - rSPosition
    cTPattern = cTPosition - cSPosition
    #print("rT, cT 888888888888888888888888888", rTPattern, cTPattern)
    if ((rTPattern == 1) or (rTPattern == -1) or (rTPattern == 0)):
        if ((cTPattern == 1) or (cTPattern == -1) or (cTPattern == 0)):
            print("""The Taminator has caught up to you.
Taminator speaks: Extension for everyone!...NOT!!!!!""")
            lossTurn = True
#    if (world[rTPosition][cTPosition] == WORK):
#        workPlace = True
#        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", workPlace)
#    if (world[rTPosition][cTPosition] == FUN):
#        funPlace = True
#        print("###############################", funPlace)
    world[rTPosition][cTPosition] = TAMINATOR
    print("workPlace, funP= ", workPlace, funPlace)
    return(rTPosition, cTPosition, lossTurn, workPlace, funPlace)

#def ():




#*****************************************************************************
def start():

    turnMode = True
    turn = 1
    funPoints = 0
    gpa = 0
    taminatorMode = False
    t_turn = 1
    world = readFromFile()
    rSPosition, cSPosition = studentPosition(world)
    workPlace = False
    funPlace = False
    print("----------------------------------------------")
    print("Current turn: ", turn)

    print("Fun points: ", funPoints, "     GPA: ", gpa)
    display(world)
    while (turnMode == True):
        selection = movementDisplay()
        world, rSPosition, cSPosition, turn, turnMode, funPoints, gpa ,  taminatorMode, rTPosition, cTPosition = movement(selection, world, rSPosition, cSPosition, funPoints, gpa, turn, turnMode, taminatorMode)
        print("rTP = ", rTPosition)

        print("taminatorMode = ", taminatorMode)
        if (taminatorMode == True):
            t_turn = t_turn + 1



            rTPosition, cTPosition, lossTurn, workPlace, funPlace = taminatorMovement(world, rTPosition, cTPosition, turn, rSPosition, cSPosition)
            if (t_turn == 4):
                taminatorMode = False
                world[rTPosition][cTPosition] = EMPTY
                print("000000000000000000", taminatorMode)
            if (lossTurn == True):
                turn = turn + 2


#            if (workPlace == True):
#                world[rTPosition][cTPosition] = WORK
#            if (funPlace == True):
#                world[rTPosition][cTPosition] = FUN
#                print("##############################################", funPlace)


        display(world)




start()





    