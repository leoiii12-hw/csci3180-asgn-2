import random
import sys


class Weapon(object):
    def __init__(self, range, damage, owner):
        """

        :type range: int
        :type damage: int
        :type owner: Player
        """
        self.range = range
        self.effect = damage
        self.owner = owner

    def action(self, posX, posY):
        """

        :type posY: int
        :type posX: int
        """
        return None

    def enhance(self):
        return None

    def getEffect(self):
        """

        :rtype: int
        """
        return self.effect

    def getRange(self):
        """

        :rtype: int
        """
        return self.range


class Axe(Weapon):
    def __init__(self, owner):
        """

        :type owner: Player
        """
        self.AXE_RANGE = 1
        self.AXE_INIT_DAMAGE = 40

        super(Axe, self).__init__(self.AXE_RANGE, self.AXE_INIT_DAMAGE, owner)

    def action(self, posX, posY):
        """

        :type posX: int
        :type posY: int
        """
        print('You are using axe attacking {0} {1}.'.format(str(posX), str(posY)))

        if self.owner.pos.distance(xy=(posX, posY)) <= self.range:
            player = self.owner.game.getPlayer(posX, posY)

            if player:
                if player.getName()[0] != self.owner.getName()[0]:
                    player.decreaseHealth(self.effect)
                else:
                    print('No cannibalism.')
        else:
            print('Out of reach.')

    def enhance(self):
        self.effect += 10


class Rifle(Weapon):
    def __init__(self, owner):
        self.RIFLE_RANGE = 4
        self.RIFLE_INIT_DAMAGE = 10

        self.AMMO_LIMIT = 6
        self.AMMO_RECHARGE = 3

        super(Rifle, self).__init__(self.RIFLE_RANGE, self.RIFLE_INIT_DAMAGE, owner)

        self.__ammo = self.AMMO_LIMIT

    def action(self, posX, posY):
        """

        :type posX: int
        :type posY: int
        """
        print('You are using rifle attacking {0} {1}.'.format(str(posX), str(posY)))
        print('Type how many ammos you want to use.')

        ammoToUse = int(raw_input())

        if ammoToUse > self.__ammo:
            print('You don\'t have that ammos.')
            return None

        if self.owner.pos.distance(xy=(posX, posY)) <= self.range:
            player = self.owner.game.getPlayer(posX, posY)

            if player:
                if player.getName()[0] != self.owner.getName()[0]:
                    player.decreaseHealth(self.effect * ammoToUse)
                    self.__ammo -= ammoToUse
                else:
                    print('No cannibalism.')
        else:
            print('Out of reach.')

    def enhance(self):
        self.__ammo = min(self.AMMO_LIMIT, self.__ammo + self.AMMO_RECHARGE)

    def getAmmo(self):
        return self.__ammo


class Pos(object):
    def __init__(self, x, y):
        """

        :type x: int
        :type y: int
        """

        self.__x = x
        self.__y = y

    def distance(self, another=None, xy=None):
        """

        :type another: Pos
        :type xy: (int,int)
        """

        if another:
            return abs(self.__x - another.__x) + abs(self.__y - another.__y)

        if xy:
            return abs(self.__x - xy[0]) + abs(self.__y - xy[1])

        return None

    def setPos(self, x, y):
        """

        :type x: int
        :type y: int
        """
        self.__x = x
        self.__y = y

    def getX(self):
        """

        :rtype: int
        """
        return self.__x

    def getY(self):
        """

        :rtype: int
        """
        return self.__y


class Player(object):
    def __init__(self, healthCap, mob, posX, posY, index, game):
        """

        :type healthCap: int
        :type mob: int
        :type posX: int
        :type posY: int
        :type index: int
        :type game: SurvivalGame
        """
        self.__mobility = mob

        self.health = healthCap
        self.pos = Pos(posX, posY)
        self.index = index
        self.game = game

        self.myString = None  # type: str
        self.equipment = None  # type: Weapon

    def getPos(self):
        """

        :rtype Pos
        """
        return self.pos

    def teleport(self):
        randX = random.randint(0, self.game.D - 1)
        randY = random.randint(0, self.game.D - 1)

        while self.game.positionOccupied(randX, randY):
            randX = random.randint(0, self.game.D - 1)
            randY = random.randint(0, self.game.D - 1)

        self.pos.setPos(randX, randY)

    def increaseHealth(self, h):
        """

        :type h: int
        """
        self.health += h

    def decreaseHealth(self, h):
        """

        :type h: int
        """
        self.health -= h
        if self.health <= 0:
            self.myString = 'C' + self.myString[0]

    def getName(self):
        """

        :rtype: str
        """
        return self.myString

    def askForMove(self):
        print('Your health is {0}. Your position is ({1},{2}). Your mobility is {3}.'.format(
            str(self.health),
            str(self.pos.getX()),
            str(self.pos.getY()),
            str(self.__mobility)))

        print('You now have following options: ')
        print('1. Move')
        print('2. Attack')
        print('3. End the turn')

        a = int(raw_input())

        if a == 1:
            print('Specify your target position (Input \'x y\').')

            typedXYStr = raw_input()
            (posX, posY) = typedXYStr.split()
            posX = int(posX)
            posY = int(posY)

            if self.pos.distance(xy=(posX, posY)) > self.__mobility:
                print('Beyond your reach. Staying still.')
            elif self.game.positionOccupied(posX, posY):
                print('Position occupied. Cannot move there.')
            else:
                self.pos.setPos(posX, posY)
                self.game.printBoard()

                print('You can now \n1.attack\n2.End the turn')
                i = int(raw_input())
                if i == 1:
                    print('Input position to attack. (Input \'x y\')')

                    typedXYStr = raw_input()
                    (attX, attY) = typedXYStr.split()
                    attX = int(attX)
                    attY = int(attY)

                    self.equipment.action(int(attX), int(attY))
        elif a == 2:
            print('Input position to attack.')

            typedXYStr = raw_input()
            (attX, attY) = typedXYStr.split()
            attX = int(attX)
            attY = int(attY)

            self.equipment.action(int(attX), int(attY))


class Chark(Player):
    def __init__(self, posX, posY, index, game):
        """

        :type posX: int
        :type posY: int
        :type index: int
        :type game: SurvivalGame
        """
        super(Chark, self).__init__(100, 4, posX, posY, index, game)

        self.myString = 'C' + str(index)
        self.equipment = Axe(self)

    def teleport(self):
        super(Chark, self).teleport()
        self.equipment.enhance() # duck typing

    def askForMove(self):
        print(
            "You are a Chark (C{0}) using Axe. (Range: {1}, Damage: {2})".format(
                self.index,
                self.equipment.getRange(),
                self.equipment.getEffect()))
        super(Chark, self).askForMove()


class Human(Player):
    def __init__(self, posX, posY, index, game):
        """

        :type posX: int
        :type posY: int
        :type index: int
        :type game: SurvivalGame
        """
        super(Human, self).__init__(80, 2, posX, posY, index, game)

        self.myString = 'H' + str(index)
        self.equipment = None  # type: Weapon

    def teleport(self):
        super(Human, self).teleport()
        self.equipment.enhance()  # duck typing

    def askForMove(self):
        print("You are a human (H{0}) using Rifle. (Range {1}, Ammo #: {2}, Damage per shot: {3})"
              .format(self.index,
                      self.equipment.getRange(),
                      self.equipment.getAmmo(), # duck typing
                      self.equipment.getEffect()))

        super(Human, self).askForMove()


class Obstacle(object):
    def __init__(self, posX, posY, index, game):
        """

        :type posX: int
        :type posY: int
        :type index: int
        :type game: SurvivalGame
        """
        self.pos = Pos(posX, posY)
        self.index = index
        self.game = game

    def getPos(self):
        """

        :rtype: Pos
        """
        return self.pos

    def teleport(self):
        randX = random.randint(0, self.game.D - 1)
        randY = self.game.D - randX - 1

        while self.game.positionOccupied(randX, randY):
            randX = random.randint(0, self.game.D - 1)
            randY = self.game.D - randX - 1

        self.pos.setPos(randX, randY)


class SurvivalGame(object):
    def __init__(self):
        self.D = 10

        self.__O = 2
        self.__n = None

        self.__teleportObjects = []

    def printBoard(self):
        printObject = []

        for i in range(self.D):
            printObject.append([])
            for j in range(self.D):
                printObject[i].append('  ')

        for i in range(self.__n):
            teleportObject = self.__teleportObjects[i]

            pos = teleportObject.getPos()  # duck typing
            printObject[pos.getX()][pos.getY()] = teleportObject.getName()

        for i in range(self.__n, self.__n + self.__O):
            teleportObject = self.__teleportObjects[i]

            pos = teleportObject.getPos()
            printObject[pos.getX()][pos.getY()] = "O" + str(i - self.__n)

        sys.stdout.write(' ')
        for i in range(self.D):
            sys.stdout.write('| {0}  '.format(i))

        sys.stdout.write('|\n')
        for i in range(int(self.D * 5.5)):
            sys.stdout.write('-')
        sys.stdout.write('\n')

        for row in range(self.D):
            sys.stdout.write(str(row))
            for col in range(self.D):
                sys.stdout.write('| {0} '.format(printObject[row][col]))
            sys.stdout.write('|\n')

            for i in range(int(self.D * 5.5)):
                sys.stdout.write('-')
            sys.stdout.write('\n')

    def positionOccupied(self, x, y):
        """

        :rtype: bool
        """
        # duck typing
        for teleportObject in self.__teleportObjects:
            pos = teleportObject.getPos()
            if pos.getX() == x and pos.getY() == y:
                return True

        return False

    def getPlayer(self, x, y):
        """

        :rtype: Player
        """
        for teleportObject in self.__teleportObjects:
            if isinstance(teleportObject, Player):
                pos = teleportObject.getPos()  # duck typing
                if pos.getX() == x and pos.getY() == y:
                    return teleportObject

        return None

    def __init(self):
        print('Welcome to Kafustrok. Light blesses you. \nInput number of players: (a even number)')

        self.__n = int(raw_input())

        self.__teleportObjects = []

        for i in range(int(self.__n / 2)):
            self.__teleportObjects.append(Human(0, 0, i, self))

        for i in range(int(self.__n / 2)):
            self.__teleportObjects.append(Chark(0, 0, i, self))

        for i in range(int(self.__O)):
            self.__teleportObjects.append(Obstacle(0, 0, i, self))

    def __gameStart(self):
        turn = 0

        while True:
            if turn == 0:
                for teleportObject in self.__teleportObjects:
                    teleportObject.teleport()  # duck typing

                print('Everything gets teleported..')

            self.printBoard()

            player = self.__teleportObjects[turn]

            if player.health > 0:
                player.askForMove()
                sys.stdout.write('\n\n')

            turn = (turn + 1) % self.__n

            numOfAliveHumans = 0
            numOfAliveCharks = 0

            for teleportObject in self.__teleportObjects:
                if isinstance(teleportObject, Human):
                    if teleportObject.health > 0:
                        numOfAliveHumans += 1

                if isinstance(teleportObject, Chark):
                    if teleportObject.health > 0:
                        numOfAliveCharks += 1

            if numOfAliveHumans == 0 or numOfAliveCharks == 0:
                break

        print('Game over.')
        self.printBoard()

    @staticmethod
    def start():
        game = SurvivalGame()
        game.__init()
        game.__gameStart()


SurvivalGame.start()
