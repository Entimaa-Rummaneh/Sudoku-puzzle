# Fanan Tamim        1180070
# Intimaa Rummaneh   1180841

import os
import random
import time

gamelist = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]]


class Player:
    def __init__(self):
        print("")

    def score(self):
        raise NotImplementedError("Subclass must implement abstract method")

    def setup(self):
        raise NotImplementedError("Subclass must implement abstract method")


class onePlayer(Player):
    __timer = 0
    __points = 0
    __playerscore = 0

    def __init__(self):
        super(Player, self).__init__()

    def score(self):
        if self.__points <= 0:
            self.__playerscore = 0
        else:
            self.__playerscore = (self.__points / 81) * (3600 / self.__timer)
        return self.__playerscore

    def get_points(self):
        return self.__points

    def set_points(self, x):
        if x == 'H':  # loss 2 points if hint
            self.__points -= 2
        elif x == 'F':  # loss 1 point if wrong fill or pass
            self.__points -= 1
        else:  # get 1 point if correct fill
            self.__points += 1

    def get_score(self):
        return self.__playerscore

    def set_score(self, playerscore):
        self.__playerscore = playerscore

    def get_time(self):
        return self.__timer

    def set_time(self, timer):
        self.__timer = timer

    def setup(self):
        # setup game from file or from random values
        choice = input("enter F for file or R for random: ")
        while (choice != 'F' and choice != 'R'):
            print("Wrong choice")
            choice = input("enter F for file or R for random: ")
        if choice == 'F':
            gameFromFile(gamelist)
        elif choice == 'R':
            gameFromRandom(gamelist)
        else:
            print("Wrong choice")
        playGame()


class twoPlayer(onePlayer):

    def __init__(self):
        super(onePlayer, self).__init__()

    def score(self, p):
        if self.get_points() <= 0:
            self.__playerscore = 0
        else:
            self.__playerscore = (self.get_points() / 81) * ((self.get_time() + p.get_time()) / self.get_time())
        return self.__playerscore

    def setup(self):
        # setup game from file or from random values
        choice = input("enter F for file or R for random: ")
        while (choice != 'F' and choice != 'R'):
            print("Wrong choice")
            choice = input("enter F for file or R for random: ")
        if choice == 'F':
            gameFromFile(gamelist)
        elif choice == 'R':
            gameFromRandom(gamelist)
        else:
            print("Wrong choice")
        playGame2()


def gameFromFile(gamelist):
    gamelist.clear()
    filename = input("enter file name: ")
    while (not os.path.isfile(filename)):
        print("File does not exist")
        filename = input("enter file name: ")
    f = open(filename, "r+")
    for line in f:
        line = line[:17]
        gamelist.append(line.split(","))

    for r in range(9):
        for c in range(9):
            if (not gamelist[r][c].isdigit()):
                gamelist[r][c] = 0
    for r in range(9):
        for c in range(9):
            gamelist[r][c] = int(gamelist[r][c])


def gameFromRandom(gamelist):
    difficulty = input("Enter E for easy, M for medium, D for difficult: ")
    while (difficulty != 'E' and difficulty != 'M' and difficulty != 'D'):
        print("Wrong choice")
        difficulty = input("Enter E for easy, M for medium, D for difficult: ")

    if (difficulty == 'E'):
        setDifficulty(32)  # 40% * 81 = 32 full squares
    elif (difficulty == 'M'):
        setDifficulty(20)  # 25% * 81 = 20 full squares
    elif (difficulty == 'D'):
        setDifficulty(8)  # 10% * 81 = 8 full squares
    else:
        print("Wrong choice")


def setDifficulty(num):
    for i in range(num):
        row = random.randint(0, 8)
        column = random.randint(0, 8)
        while (gamelist[row][column] != 0):
            row = random.randint(0, 8)
            column = random.randint(0, 8)
        value = random.randint(1, 9)
        while not isvalid(value, row, column):
            value = random.randint(1, 9)
        gamelist[row][column] = value


def is_used_in_row(n, r):
    for i in range(9):
        if gamelist[r][i] == n:
            return True
    return False


def is_used_in_column(n, c):
    for i in range(9):
        if gamelist[i][c] == n:
            return True
    return False


def is_used_in_box(n, r, c):
    box_r = 3 * (r // 3)
    box_c = 3 * (c // 3)
    for i in range(3):
        for j in range(3):
            if gamelist[box_r + i][box_c + j] == n:
                return True
    return False


def isvalid(value, row, column):
    # check row
    if not is_used_in_row(value, row):
        # check column
        if not is_used_in_column(value, column):
            # check box
            if not is_used_in_box(value, row, column):
                return True
    return False


def printsudoku():
    for i in range(9):
        line = ""
        if i == 3 or i == 6:
            print("---------------------")
        for j in range(9):
            if j == 3 or j == 6:
                line += "| "
            if gamelist[i][j] == 0:
                line += "." + " "
            else:
                line += str(gamelist[i][j]) + " "
        print(line)


def playGame():
    print("Hello Player, Please choose from the following options")
    start = time.time()
    while not is_full():
        printsudoku()
        choice = input("Enter F for Fill, H for Hint, S for Solve, Q for quit: ")
        if choice == 'F':
            fill(p1)
        elif choice == 'H':
            hint()
            p1.set_points('H')
        elif choice == 'S':
            if Suduko(gamelist, 0, 0):
                printsudoku()
            else:
                print("Solution does not exist")
            exit(0)
        elif choice == 'Q':
            exit(0)
        else:
            print("Wrong choice")
        print("points: " + str(p1.get_points()))
    printsudoku()
    end = time.time()
    alltime = end - start
    p1.set_time(alltime)
    print("You win")
    print("score: " + str(p1.score()))


def playGame2():
    print("Hello Players, Please choose from the following options")
    pass1 = 0
    pass2 = 0
    timer1 = 0
    timer2 = 0
    while not is_full():
        printsudoku()
        start1 = time.time()
        choice = input("PLAYER1: Enter F for Fill, P for pass, S for Solve, Q for quit: ")
        while (choice != 'F' and choice != 'P' and choice != 'S' and choice != 'Q'):
            print("Wrong choice")
            choice = input("PLAYER1: Enter F for Fill, P for pass, S for Solve, Q for quit: ")
        if choice == 'F':
            fill(p1)
        elif choice == 'P':
            p1.set_points('F')
            if pass2 == 0:
                pass1 = 0
            pass1 += 1
            pass
        elif choice == 'S':
            if Suduko(gamelist, 0, 0):
                printsudoku()
            else:
                print("Solution does not exist")
            exit(0)
        elif choice == 'Q':
            exit(0)
        else:
            print("Wrong choice")
        end1 = time.time()
        alltime1 = end1 - start1
        timer1 += alltime1
        print("Player 1 points: " + str(p1.get_points()) + "                " + "Player 2 points: " + str(
            p2.get_points()))
        printsudoku()

        if is_full():
            break
        if (pass1 == 2 and pass2 == 2):
            hint()
            pass1 = 0
            pass2 = 0

        start2 = time.time()
        choice = input("PLAYER2: Enter F for Fill, P for Pass, S for Solve, Q for quit: ")
        while (choice != 'F' and choice != 'P' and choice != 'S' and choice != 'Q'):
            print("Wrong choice")
            choice = input("PLAYER2: Enter F for Fill, P for pass, S for Solve, Q for quit: ")
        if choice == 'F':
            fill(p2)
        elif choice == 'P':
            p2.set_points('F')
            if (pass1 == 0):
                pass2 = 0
            pass2 += 1
            pass
        elif choice == 'S':
            if (Suduko(gamelist, 0, 0)):
                printsudoku()
            else:
                print("Solution does not exist")
            exit(0)
        elif (choice == 'Q'):
            exit(0)
        else:
            print("Wrong choice")
        end2 = time.time()

        alltime2 = end2 - start2
        timer2 += alltime2
        print("Player 1 points: " + str(p1.get_points()) + "                " + "Player 2 points: " + str(
            p2.get_points()))
        if (pass1 == 2 and pass2 == 2):  # If the Pass option is requested by the two players for 2 times in sequence
            hint()
            pass1 = 0
            pass2 = 0
    p1.set_time(timer1)
    p2.set_time(timer2)
    print("Player 1 score: " + str(p1.score(p2)) + "                " + "Player 2 score: " + str(p2.score(p1)))
    if ((p1.score(p2)) > p2.score(p1)):
        print("Player 1 is the winner")
    else:
        print("Player 2 is the winner")


def fill(p):
    print("Note: row and column from 0 to 8")
    line = input("enter row, column, value as: r c v ")
    t = tuple(line.split())
    row = int(t[0])
    column = int(t[1])
    value = int(t[2])
    while ((not 0 <= row <= 8) or (not 0 <= column <= 8) or (not 1 <= value <= 9)):
        print("Wrong values")
        print("Note: row and column from 0 to 8")
        line = input("enter row, column, value as: r c v ")
        t = tuple(line.split())
        row = int(t[0])
        column = int(t[1])
        value = int(t[2])
    if (gamelist[row][column] != 0):
        print("Not empty cell")
    elif (not isvalid(value, row, column)):
        print("wrong fill")
        p.set_points('F')
    else:
        gamelist[row][column] = value
        print("correct fill")
        p.set_points('T')


def hint():
    row = random.randint(0, 8)
    column = random.randint(0, 8)
    while (gamelist[row][column] != 0):
        row = random.randint(0, 8)
        column = random.randint(0, 8)
    value = random.randint(1, 9)
    while not isvalid(value, row, column):
        value = random.randint(1, 9)
    gamelist[row][column] = value
    print("insert value: " + str(value) + " into row: " + str(row) + " and column: " + str(column))


M = 9


def solve(gamelist, r, c, value):
    for x in range(9):
        if gamelist[r][x] == value:
            return False

    for x in range(9):
        if gamelist[x][c] == value:
            return False

    startRow = r - r % 3
    startCol = c - c % 3
    for i in range(3):
        for j in range(3):
            if gamelist[i + startRow][j + startCol] == value:
                return False
    return True


def Suduko(gamelist, r, c):
    if (r == M - 1 and c == M):
        return True
    if c == M:
        r += 1
        c = 0
    if gamelist[r][c] > 0:
        return Suduko(gamelist, r, c + 1)
    for num in range(1, M + 1, 1):

        if solve(gamelist, r, c, num):

            gamelist[r][c] = num
            if Suduko(gamelist, r, c + 1):
                return True
        gamelist[r][c] = 0
    return False


def is_full():
    for r in range(9):
        for c in range(9):
            if (gamelist[r][c] == 0):
                return False
    return True


mode = input("enter O for one player or T for two players: ")
while (mode != 'O' and mode != 'T'):
    print("Wrong choice")
    mode = input("enter O for one player or T for two players: ")
if mode == 'O':
    p1 = onePlayer()
    p1.setup()
elif mode == 'T':
    p1 = twoPlayer()
    p2 = twoPlayer()
    p1.setup()
else:
    print("Wrong choice")
