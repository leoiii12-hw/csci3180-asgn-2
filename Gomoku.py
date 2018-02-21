import random
import sys


class PlayerChoice:
    Human = 1
    Computer = 2


class Gomoku(object):
    def __init__(self):
        self.numOfRows = 9
        self.numOfColumns = 9

        self.gameBoard = None

        self.player1 = None
        self.player2 = None
        self.turn = self.player1

        self.startGame()

    def startGame(self):
        self.gameBoard = GameBoard(self.numOfRows, self.numOfColumns)

        self.player1 = self.createPlayer('O', 1)
        self.player2 = self.createPlayer('X', 2)
        self.turn = self.player1

        print('Gomoku started.')

        self.printGameBoard()

        while True:
            nextMove = self.turn.nextMove()
            self.gameBoard.putCell(nextMove[0], nextMove[1], self.turn.playerSymbol)

            winningPlayer, winningPositions = self.getWinningPlayerAndPositions()
            if winningPlayer:
                self.printGameBoard(winningPositions)

                print('Player ' + str(winningPlayer.playerSymbol) + ' Win!')
                break

            if self.checkTie():
                self.printGameBoard(winningPositions)

                print('Tie')
                break

            self.switchPlayer()
            self.printGameBoard([nextMove])

    def switchPlayer(self):
        if self.turn == self.player1:
            self.turn = self.player2
        else:
            self.turn = self.player1

    def createPlayer(self, playerSymbol, playerNum):
        if playerSymbol != 'O' and playerSymbol != 'X':
            print('The playerSymbol is invalid.')
            return

        if playerNum != 1 and playerNum != 2:
            print('The playerNum is invalid.')
            return

        print('')
        print('Please choose player ' + str(playerNum) + ' (' + playerSymbol + '):')
        print('1. Human')
        print('2. Computer Player')
        playerChoice = input('Your choice is: ')

        if playerChoice == PlayerChoice.Human:
            print('Player ' + playerSymbol + ' is Human.')
            return Human(playerSymbol, self.gameBoard)
        if playerChoice == PlayerChoice.Computer:
            print('Player ' + playerSymbol + ' is Computer.')
            return Computer(playerSymbol, self.gameBoard)

    def printGameBoard(self, highlightingPositions=None):
        if highlightingPositions is None:
            highlightingPositions = []

        sys.stdout.write('\n')

        # header
        sys.stdout.write('   |')
        for i in range(self.numOfColumns):
            sys.stdout.write(' ' + str(i + 1) + ' |')
        sys.stdout.write('\n')

        # header separator
        sys.stdout.write('----')
        for i in range(self.numOfColumns):
            sys.stdout.write('----')
        sys.stdout.write('\n')

        for i in range(self.numOfRows):
            # real cells
            sys.stdout.write(' ' + str(i + 1) + ' |')
            for j in range(self.numOfColumns):
                if (i, j) in highlightingPositions:
                    sys.stdout.write('*' + str(self.gameBoard.getCell(i, j)) + '*|')
                else:
                    sys.stdout.write(' ' + str(self.gameBoard.getCell(i, j)) + ' |')
            sys.stdout.write('\n')

            # row separator
            sys.stdout.write('----')
            for j in range(self.numOfColumns):
                sys.stdout.write('----')
            sys.stdout.write('\n')

        sys.stdout.write('\n')

        sys.stdout.flush()

    def getWinningPlayerAndPositions(self):
        occupiedPositions = self.gameBoard.getOccupiedPositions()

        for position in occupiedPositions:
            checkWinResult = self.__checkWin(position, 5, self.player1.playerSymbol)
            if checkWinResult:
                return self.player1, checkWinResult

            checkWinResult = self.__checkWin(position, 5, self.player2.playerSymbol)
            if checkWinResult:
                return self.player2, checkWinResult

        return None, None

    def __checkWin(self, position, depth, playerSymbol):
        def left(p, b):
            return p[0] + b, p[1]

        def right(p, b):
            return p[0] + b, p[1]

        def top(p, b):
            return p[0], p[1] - b

        def bottom(p, b):
            return p[0], p[1] + b

        def leftTop(p, b):
            return left(top(p, b), b)

        def rightTop(p, b):
            return right(top(p, b), b)

        def leftBottom(p, b):
            return left(bottom(p, b), b)

        def rightBottom(p, b):
            return right(bottom(p, b), b)

        positionMethod = [left, right, top, bottom, leftTop, rightTop, leftBottom, rightBottom]

        breaths = range(depth)
        breaths.reverse()

        for method in positionMethod:
            winningPositions = []

            for breath in breaths:
                validatingPosition = method(position, breath)

                if self.gameBoard.getCell(validatingPosition[0], validatingPosition[1]) != playerSymbol:
                    break
                else:
                    winningPositions.append(validatingPosition)

                    if breath == 0:
                        return winningPositions

        return False

    def checkTie(self):
        return len(self.gameBoard.getEmptyPositions()) == 0


class GameBoard(object):
    def __init__(self, numOfRows, numOfColumns):
        self.numOfRows = numOfRows
        self.numOfColumns = numOfColumns
        self.gameBoard = []

        for i in range(numOfRows):
            self.gameBoard.append([])
            for j in range(numOfColumns):
                self.gameBoard[i].append(' ')

    def isOutOfBoard(self, row, column):
        if row >= self.numOfRows or row < 0 or \
                column >= self.numOfColumns or column < 0:
            return True

        return False

    def getCell(self, row, column):
        if self.isOutOfBoard(row, column):
            return False

        return self.gameBoard[row][column]

    def putCell(self, row, column, playerSymbol):
        if self.isOutOfBoard(row, column):
            return False

        if playerSymbol == 'W':
            self.gameBoard[row][column] = playerSymbol
            return False

        if not self.isOccupied(row, column):
            self.gameBoard[row][column] = playerSymbol
        else:
            sys.exit('Invalid putCell')

    def isOccupied(self, row, column):
        if self.isOutOfBoard(row, column):
            return False

        return self.getCell(row, column) != ' '

    def getEmptyPositions(self):
        emptyPositions = []

        for i in range(self.numOfRows):
            for j in range(self.numOfColumns):
                if not self.isOccupied(i, j):
                    emptyPositions.append((i, j))

        return emptyPositions

    def getOccupiedPositions(self):
        occupiedPositions = []

        for i in range(self.numOfRows):
            for j in range(self.numOfColumns):
                if self.isOccupied(i, j):
                    occupiedPositions.append((i, j))

        return occupiedPositions


class Player(object):
    def __init__(self, playerSymbol, gameBoard):
        self.playerSymbol = playerSymbol
        self.gameBoard = gameBoard

    def nextMove(self):
        return 0, 0

    def toString(self):
        return 'Player'


class Human(Player):
    def nextMove(self):
        while True:
            print('Player ' + self.playerSymbol + '\'s turn!')

            typedRowAndColStr = raw_input("Type the row and col to put the disc: ")
            typedRowAndColList = typedRowAndColStr.split()

            if len(typedRowAndColList) == 2:
                typedRowAndCol = (int(typedRowAndColList[0]) - 1, int(typedRowAndColList[1]) - 1)

                if self.gameBoard.isOccupied(typedRowAndCol[0], typedRowAndCol[1]) or \
                        self.gameBoard.isOutOfBoard(typedRowAndCol[0], typedRowAndCol[1]):
                    print('Invalid input!')
                    continue

                return typedRowAndCol[0], typedRowAndCol[1]

    def toString(self):
        return 'Human'


class Computer(Player):
    def nextMove(self):
        print('Player ' + self.playerSymbol + '\'s turn!')

        emptyPositions = self.gameBoard.getEmptyPositions()

        if len(emptyPositions) > 0:
            return random.choice(emptyPositions)

    def toString(self):
        return 'Computer'


Gomoku()
