import copy
import math
import random


# exceptions

"""
Systeme d'inventaire < à 10 item 1pt
Systeme d'experience 1pt
Systeme de déplacement en diagonale 1pt
Systeme de nourriture 1pt 
Systeme de poison 1pt
Systeme de magie partie 1 2pts
"""


def _find_getch():
    """Single char input, only works only on mac/linux/windows OS terminals"""
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return lambda: msvcrt.getch().decode('utf-8')
    # POSIX system. Create and return a getch that manipulates the tty.
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch


def sign(x):
    if x > 0:
        return 1
    return -1


class Coord(object):
    """Implementation of a map coordinate"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '<' + str(self.x) + ',' + str(self.y) + '>'

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

    def distance(self, other):
        """Returns the distance between two coordinates."""
        d = self - other
        return math.sqrt(d.x * d.x + d.y * d.y)

    def direction(self, other):
        """Returns the direction between two coordinates."""
        d = self - other
        cos = d.x / self.distance(other)
        cos45 = 1 / math.sqrt(2)

        if cos > cos45:  # gauche
            if d.y > 0:  # haut
                # diagonale en haut à gauche
                return Coord(-1, -1)
            elif d.y < 0:
                return Coord(-1, 1)
            return Coord(-1, 0)


        elif cos < -cos45:  # droite
            if d.y > 0:  # haut
                # diagonale en haut à droite
                return Coord(1, -1)
            elif d.y < 0:
                return Coord(1, 1)
            return Coord(1, 0)




        elif d.y > 0:  # haut
            return Coord(0, -1)

        else:
            return Coord(0, 1)


'''
'x': lambda h: theGame()._floor.move(h,Coord(1,1)),\
'w': lambda h: theGame()._floor.move(h,Coord(-1,1)),\
                'e': lambda h: theGame()._floor.move(h,Coord(1,-1)),\
                'a': lambda h: theGame()._floor.move(h,Coord(-1,-1)),\
                '''


class Element(object):
    """Base class for game elements. Have a name.
        Abstract class."""

    def __init__(self, name, abbrv=""):
        self.name = name
        if abbrv == "":
            abbrv = name[0]
        self.abbrv = abbrv

    def __repr__(self):
        return self.abbrv

    def description(self):
        """Description of the element"""
        return "<" + self.name + ">"

    def meet(self, hero):
        """Makes the hero meet an element. Not implemented. """
        raise NotImplementedError('Abstract Element')


class Creature(Element):
    """A creature that occupies the dungeon.
        Is an Element. Has hit points and strength."""

    def __init__(self, name, hp, abbrv="", strength=1):
        Element.__init__(self, name, abbrv)
        self.hp = hp
        self.strength = strength

    def description(self):
        """Description of the creature"""
        return Element.description(self) + "(" + str(self.hp) + ")"

    def meet(self, other):
        """The creature is encountered by an other creature.
            The other one hits the creature. Return True if the creature is dead."""
        self.hp -= other.strength
        theGame().addMessage("The " + other.name + " hits the " + self.description())
        if self.name == "Spider":
            other.poisoned = True
        if self.hp > 0:
            return False
        if isinstance(other, Hero):
            other.gainXP()

        return True

    def takeArrow(self, damage):
        self.hp -= damage
        if self.hp == 0:
            theGame().addMessage("The " + self.name + " is dead.")
            theGame()._floor.rm(theGame()._floor._elem[self])
            return True


class Hero(Creature):
    """The hero of the game.
        Is a creature. Has an inventory of elements. """

    def __init__(self, name="Hero", hp=10, abbrv="@", strength=2):
        Creature.__init__(self, name, hp, abbrv, strength)
        self._inventory = []
        self._or = 0
        self._xp = 0
        self._level = 0
        self._maxHP = 10
        self._mpMax = 20
        self._mp = 20
        self._sorts = [(0, "TP"), (1, "Soin"), (2, "Invisibilite")]
        self._isInvis = False
        self.hunger = 20
        self.poisoned = False

    def description(self):
        """Description of the hero"""
        return Creature.description(self) + str(self._inventory) + str(self._or)

    def getMP(self):
        return self._mp

    def getSorts(self):
        return self._sorts

    def getInvis(self):
        return self._isInvis

    def setInvis(self, val):
        self._isInvis = val

    def fullDescription(self):
        """Complete description of the hero"""
        res = ''
        for e in self.__dict__:
            if e[0] != '_':
                res += '> ' + e + ' : ' + str(self.__dict__[e]) + '\n'
        res += '> INVENTORY : ' + str([x.name for x in self._inventory])
        return res

    def checkEquipment(self, o):
        """Check if o is an Equipment."""
        if not isinstance(o, Equipment):
            raise TypeError('Not a Equipment')

    def take(self, elem):
        """The hero takes adds the equipment to its inventory"""
        self.checkEquipment(elem)
        if elem.abbrv != "o" and len(self._inventory) < 10:
            self._inventory.append(elem)

        else:
            self._or += 1

    def useMagic(self, elem):
        """Use a sort"""
        if elem is None: return

        if self._mp >= 10:
            self._mp -= 10
            if (elem == 0):
                """TP"""
                self.teleport()
                print("Vous vous etes teleportes \n")
            elif (elem == 1):
                """Soin"""
                self.heal(self._maxHP)
                print("Vous avez ete soigne \n")
            elif (elem == 2):
                """Invisibility"""
                self._isInvis = True
                print("Vous etes invisibles  \n")
            else:
                print("error")
            print("Nombre de MP restants : ", self._mp, "/20 \n")
        else:
            print("Vous n'avez pas assez de mp \n")

    def use(self, elem):
        """Use a piece of equipment"""
        if elem is None:
            return
        self.checkEquipment(elem)
        if elem not in self._inventory:
            raise ValueError('Equipment ' + elem.name + 'not in inventory')
        if elem.use(self):
            self._inventory.remove(elem)

    def throw(self, elem):
        """Throw an element"""
        if elem is None:
            return
        print("Choisir une direction : d=droite, q=gauche, z=haut, s=bas")
        c = getch()
        if c in ['d', 'q', 'z', 's']:
            Arrow.goToDirection(elem, c, self)

    def heal(self, hp):
        """Heal the hero"""
        self.hp += hp
        self._mp = self._mpMax
        self.hunger = 20
        self.poisoned = False
        if self.hp > self._maxHP:
            self.hp = self._maxHP

    def teleport(self):
        """Teleport the hero"""
        r = theGame()._floor.randRoom()
        c = r.randCoord()
        theGame()._floor.rm(theGame()._floor.pos(self))
        theGame()._floor.put(c, self)
    def setStrength(self, val):
        self.strength=val
    def gainLvl(self):
        self._xp -= 100
        self._level += 1
        print(" Le hero a gagne un level ! \n Il est desormais level :", self._level, "\n")
        self.gainStats()

    def gainXP(self):
        self._xp += 20
        print(" Le hero a gagne 20 xp, \n il a desormais ", self._xp, "/100 xp")
        if self._xp >= 100:
            self.gainLvl()

    def gainStats(self):
        self._maxHP += 5
        self.strength += 2
        self.heal(self._maxHP)
        self._mpMax += 10
        self.mp = self._mpMax
        print(
            " Le hero a gagne 2 de force , 10 manaPoints max et 5 HP max supplementaires \n ses statistiques actuelles sont : ",
            self.strength, " ", self._maxHP, " ", self._maxHP)


class Equipment(Element):
    """A piece of equipment"""

    def __init__(self, name, abbrv="", usage=None):
        Element.__init__(self, name, abbrv)
        self.usage = usage

    def meet(self, hero):
        """Makes the hero meet an element. The hero takes the element."""
        hero.take(self)
        theGame().addMessage("You pick up a " + self.name)
        return True

    def use(self, creature):
        """Uses the piece of equipment. Has effect on the hero according usage.
            Return True if the object is consumed."""
        if self.usage is None:
            theGame().addMessage("The " + self.name + " is not usable")
            return False
        else:
            theGame().addMessage("The " + creature.name + " uses the " + self.name)
            return self.usage(self, creature)


class Stairs(Element):
    """ Strairs that goes down one floor. """

    def __init__(self):
        super().__init__("Stairs", 'E')

    def meet(self, hero):
        """Goes down"""
        theGame().buildFloor()
        theGame().addMessage("The " + hero.name + " goes down")


class Room(object):
    """A rectangular room in the map"""

    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2

    def __repr__(self):
        return "[" + str(self.c1) + ", " + str(self.c2) + "]"

    def __contains__(self, coord):
        return self.c1.x <= coord.x <= self.c2.x and self.c1.y <= coord.y <= self.c2.y

    def intersect(self, other):
        """Test if the room has an intersection with another room"""
        sc3 = Coord(self.c2.x, self.c1.y)
        sc4 = Coord(self.c1.x, self.c2.y)
        return self.c1 in other or self.c2 in other or sc3 in other or sc4 in other or other.c1 in self

    def center(self):
        """Returns the coordinates of the room center"""
        return Coord((self.c1.x + self.c2.x) // 2, (self.c1.y + self.c2.y) // 2)

    def randCoord(self):
        """A random coordinate inside the room"""
        return Coord(random.randint(self.c1.x, self.c2.x), random.randint(self.c1.y, self.c2.y))

    def randEmptyCoord(self, map):
        """A random coordinate inside the room which is free on the map."""
        c = self.randCoord()
        while map.get(c) != Map.ground or c == self.center():
            c = self.randCoord()
        return c

    def decorate(self, map):
        """Decorates the room by adding a random equipment and monster."""
        map.put(self.randEmptyCoord(map), theGame().randEquipment())
        map.put(self.randEmptyCoord(map), theGame().randMonster())


class Map(object):
    """A map of a game floor.
        Contains game elements."""

    ground = '.'  # A walkable ground cell
    dir = {'z': Coord(0, -1), 's': Coord(0, 1), 'd': Coord(1, 0), 'q': Coord(-1, 0)}  # four direction user keys
    empty = ' '  # A non walkable cell

    def __init__(self, size=20, hero=None):
        self.debut = 0
        self.fin = 3
        self._mat = []
        self._elem = {}
        self._rooms = []
        self._roomsToReach = []
        self._nbTours = 0
        for i in range(size):
            self._mat.append([Map.empty] * size)
        if hero is None:
            hero = Hero()
        self._hero = hero
        self.generateRooms(7)
        self.reachAllRooms()
        self.put(self._rooms[0].center(), hero)
        for r in self._rooms:
            r.decorate(self)

    def addRoom(self, room):
        """Adds a room in the map."""
        self._roomsToReach.append(room)
        for y in range(room.c1.y, room.c2.y + 1):
            for x in range(room.c1.x, room.c2.x + 1):
                self._mat[y][x] = Map.ground

    def getElem(self):
        return self._elem

    def findRoom(self, coord):
        """If the coord belongs to a room, returns the room elsewhere returns None"""
        for r in self._roomsToReach:
            if coord in r:
                return r
        return None

    def intersectNone(self, room):
        """Tests if the room shall intersect any room already in the map."""
        for r in self._roomsToReach:
            if room.intersect(r):
                return False
        return True

    def dig(self, coord):
        """Puts a ground cell at the given coord.
            If the coord corresponds to a room, considers the room reached."""
        self._mat[coord.y][coord.x] = Map.ground
        r = self.findRoom(coord)
        if r:
            self._roomsToReach.remove(r)
            self._rooms.append(r)

    def corridor(self, cursor, end):
        """Digs a corridors from the coordinates cursor to the end, first vertically, then horizontally."""
        d = end - cursor
        self.dig(cursor)
        while cursor.y != end.y:
            cursor = cursor + Coord(0, sign(d.y))
            self.dig(cursor)
        while cursor.x != end.x:
            cursor = cursor + Coord(sign(d.x), 0)
            self.dig(cursor)

    def reach(self):
        """Makes more rooms reachable.
            Start from one random reached room, and dig a corridor to an unreached room."""
        roomA = random.choice(self._rooms)
        roomB = random.choice(self._roomsToReach)

        self.corridor(roomA.center(), roomB.center())

    def reachAllRooms(self):
        """Makes all rooms reachable.
            Start from the first room, repeats @reach until all rooms are reached."""
        self._rooms.append(self._roomsToReach.pop(0))
        while len(self._roomsToReach) > 0:
            self.reach()

    def randRoom(self):
        """A random room to be put on the map."""
        c1 = Coord(random.randint(0, len(self) - 3), random.randint(0, len(self) - 3))
        c2 = Coord(min(c1.x + random.randint(3, 8), len(self) - 1), min(c1.y + random.randint(3, 8), len(self) - 1))
        return Room(c1, c2)

    def generateRooms(self, n):
        """Generates n random rooms and adds them if non-intersecting."""
        for i in range(n):
            r = self.randRoom()
            if self.intersectNone(r):
                self.addRoom(r)

    def __len__(self):
        return len(self._mat)

    def __contains__(self, item):
        if isinstance(item, Coord):
            return 0 <= item.x < len(self) and 0 <= item.y < len(self)
        return item in self._elem

    def __repr__(self):
        s = ""
        for i in self._mat:
            for j in i:
                s += str(j)
            s += '\n'
        return s

    def checkCoord(self, c):
        """Check if the coordinates c is valid in the map."""
        if not isinstance(c, Coord):
            raise TypeError('Not a Coord')
        if not c in self:
            return False
            raise IndexError('Out of map coord')

    def checkElement(self, o):
        """Check if o is an Element."""
        if not isinstance(o, Element):
            raise TypeError('Not a Element')

    def put(self, c, o):
        """Puts an element o on the cell c"""
        self.checkCoord(c)
        self.checkElement(o)
        if self._mat[c.y][c.x] != Map.ground:
            raise ValueError('Incorrect cell')
        if o in self._elem:
            raise KeyError('Already placed')
        self._mat[c.y][c.x] = o
        self._elem[o] = c

    def get(self, c):
        """Returns the object present on the cell c"""
        if self.checkCoord(c):
            return False
        else:
            return self._mat[c.y][c.x]

    def pos(self, o):
        """Returns the coordinates of an element in the map """
        self.checkElement(o)
        return self._elem[o]

    def rm(self, c):
        """Removes the element at the coordinates c"""
        self.checkCoord(c)
        del self._elem[self._mat[c.y][c.x]]
        self._mat[c.y][c.x] = Map.ground

    def move(self, e, way):
        """Moves the element e in the direction way."""
        orig = self.pos(e)
        dest = orig + way

        if dest in self:
            if (isinstance(e, Hero)):
                # Systeme d'invis d'un héro:
                if Hero.getInvis(e) and self.fin > self.debut:
                    self.debut += 1
                else:
                    self.debut = 0
                    Hero.setInvis(e, False)

                if (isinstance(self.get(dest), Creature) and Hero.getInvis(e)):
                    Hero.setInvis(e, False)
                    self.debut = 0
                # systeme de nourriture :
                # -1 nourriture tous les 2 moves
                if self._nbTours / 5 == int(self._nbTours / 5) and e.hunger > 0:
                    e.hunger -= 1
                    print("Vous avez : ", e.hunger, " nourriture")
                elif e.hunger == 0:
                    e.hp -= 1
                    print("Vous n'avez plus assez de nourriture et vous perdez de la vie  HP restants : ", e.hp)
                # Systeme d'empoisonnement :
                if e.poisoned:
                    e.hp -= 1
                    print("Vous etes empoisonnes, vous perdez 1HP par actions. Veuillez prendre une potion")

            if self.get(dest) == Map.ground:
                self._mat[orig.y][orig.x] = Map.ground
                self._mat[dest.y][dest.x] = e
                self._elem[e] = dest
            elif self.get(dest) != Map.empty and self.get(dest).meet(e) and self.get(dest) != self._hero:

                self.rm(dest)
        self._nbTours += 1

    def moveAllMonsters(self):
        """Moves all monsters in the map.
            If a monster is at distance lower than 6 from the hero, the monster advances."""
        if (not self._hero._isInvis):
            h = self.pos(self._hero)
            for e in self._elem:
                c = self.pos(e)
                if isinstance(e, Creature) and e != self._hero and c.distance(h) < 6:
                    d = c.direction(h)
                    if self.get(c + d) in [Map.ground, self._hero]:
                        if e.name == "Dragon" or e.name == "Ork" or e.name == "Blat":
                            dd = c.direction(h) + c.direction(h)
                            if self.get(c + dd) == Map.ground:
                                self.move(e, dd)
                            elif self.get(c + dd) == self._hero:
                                self.move(e, d)
                        else:
                            self.move(e, d)


class Arrow(Element):
    """An arrow that can be used to kill a monster."""

    def __init__(self, name, damage):
        super().__init__(name)
        self._damage = damage
        self._hero = None

    def meet(self, e):
        """Kills the monster e."""
        if isinstance(e, Creature):
            e.hp -= self._damage
            if e.hp <= 0:
                theGame()._floor.rm(theGame()._floor.pos(e))
                theGame()._floor.rm(theGame()._floor.pos(self))
                return True
        return False

    def goToDirection(self, d, hero):
        """Moves the arrow in the direction d."""
        self._hero = hero
        print(type(self))
        print(theGame().getFloor().getElem())
        print(theGame().getFloor().getElem()[hero].x)
        print("You shoot an arrow in the direction " + d)

        if d == "z":
            dest = Coord(theGame().getFloor().getElem()[hero].x, theGame().getFloor().getElem()[hero].y - 1)
            if isinstance(theGame().getFloor().get(dest), Creature):
                print(theGame().getFloor().get(dest).name + "monstre touché")
                theGame().getFloor().get(dest).takeArrow(self._damage)
            else:
                theGame().getFloor().put(dest, self)
                dest = Coord(theGame().getFloor().getElem()[self].x, theGame().getFloor().getElem()[self].y - 1)
                while theGame().getFloor().get(dest) != False and theGame().getFloor().get(dest) == Map.ground:
                    print("Deplacement de la fleche")
                    theGame().getFloor().move(self, Coord(0, -1))
                    dest = Coord(theGame().getFloor().getElem()[self].x, theGame().getFloor().getElem()[self].y - 1)
                    print(theGame().getFloor().pos(self))
                if isinstance(theGame().getFloor().get(dest), Creature):
                    theGame().getFloor().get(dest).takeArrow(self._damage)
                    # theGame().getFloor().rm(theGame().getFloor().getElem()[self])
                    print(theGame().getFloor().get(dest).name + "monstre touché")
                else:
                    if theGame().getFloor().get(dest) != Map.ground:
                        print("La flèche n'a rien touché")
                theGame().getFloor().rm(theGame().getFloor().getElem()[self])
        if d == "s":
            dest = Coord(theGame().getFloor().getElem()[hero].x, theGame().getFloor().getElem()[hero].y + 1)
            if isinstance(theGame().getFloor().get(dest), Creature):
                print(theGame().getFloor().get(dest).name + "monstre touché")
                theGame().getFloor().get(dest).takeArrow(self._damage)
            else:
                theGame().getFloor().put(dest, self)
                dest = Coord(theGame().getFloor().getElem()[self].x, theGame().getFloor().getElem()[self].y + 1)
                while theGame().getFloor().get(dest) != False and theGame().getFloor().get(dest) == Map.ground:
                    print("Deplacement de la fleche")
                    theGame().getFloor().move(self, Coord(0, 1))
                    dest = Coord(theGame().getFloor().getElem()[self].x, theGame().getFloor().getElem()[self].y + 1)
                    print(theGame().getFloor().pos(self))
                if isinstance(theGame().getFloor().get(dest), Creature):
                    print(theGame().getFloor().get(dest).name + "monstre touché")
                    theGame().getFloor().get(dest).takeArrow(self._damage)
                    # theGame().getFloor().rm(theGame().getFloor().getElem()[self])
                else:
                    if theGame().getFloor().get(dest) != Map.ground:
                        print("La flèche n'a rien touché")
                theGame().getFloor().rm(theGame().getFloor().getElem()[self])
        if d == "q":
            dest = Coord(theGame().getFloor().getElem()[hero].x - 1, theGame().getFloor().getElem()[hero].y)
            if isinstance(theGame().getFloor().get(dest), Creature):
                print(theGame().getFloor().get(dest).name + "monstre touché")
                theGame().getFloor().get(dest).takeArrow(self._damage)

            else:
                theGame().getFloor().put(dest, self)
                dest = Coord(theGame().getFloor().getElem()[self].x - 1, theGame().getFloor().getElem()[self].y)
                while theGame().getFloor().get(dest) != False and theGame().getFloor().get(dest) == Map.ground:
                    print("Deplacement de la fleche")
                    theGame().getFloor().move(self, Coord(-1, 0))
                    dest = Coord(theGame().getFloor().getElem()[self].x - 1, theGame().getFloor().getElem()[self].y)
                    print(theGame().getFloor().pos(self))
                if isinstance(theGame().getFloor().get(dest), Creature):
                    print(theGame().getFloor().get(dest).name + "monstre touché")
                    theGame().getFloor().get(dest).takeArrow(self._damage)
                    # theGame().getFloor().rm(theGame().getFloor().getElem()[self])

                else:
                    if theGame().getFloor().get(dest) != Map.ground:
                        print("La flèche n'a rien touché")
                theGame().getFloor().rm(theGame().getFloor().getElem()[self])
        if d == "d":
            dest = Coord(theGame().getFloor().getElem()[hero].x + 1, theGame().getFloor().getElem()[hero].y)
            if isinstance(theGame().getFloor().get(dest), Creature):
                print(theGame().getFloor().get(dest).name + "monstre touché")
                theGame().getFloor().get(dest).takeArrow(self._damage)

            else:
                theGame().getFloor().put(dest, self)
                dest = Coord(theGame().getFloor().getElem()[self].x + 1, theGame().getFloor().getElem()[self].y)
                while theGame().getFloor().get(dest) != False and theGame().getFloor().get(dest) == Map.ground:
                    print("Deplacement de la fleche")
                    theGame().getFloor().move(self, Coord(1, 0))
                    dest = Coord(theGame().getFloor().getElem()[self].x + 1, theGame().getFloor().getElem()[self].y)
                    print(theGame().getFloor().pos(self))
                if isinstance(theGame().getFloor().get(dest), Creature):
                    print(theGame().getFloor().get(dest).name + "monstre touché")
                    theGame().getFloor().get(dest).takeArrow(self._damage)
                    # theGame().getFloor().rm(theGame().getFloor().getElem()[self])

                else:
                    if theGame().getFloor().get(dest) != Map.ground:
                        print("La flèche n'a rien touché")
                theGame().getFloor().rm(theGame().getFloor().getElem()[self])


class Game(object):
    """ Class representing game state """

    """ available equipments """
    equipments = {0: [Equipment("potion", "!", usage=lambda self, hero: Hero.heal(hero, 10)), Equipment("gold", "o") , Equipment("Knife", "|", usage=lambda self, hero: Hero.setStrength(4))],
                  1: [Equipment("potion", "!", usage=lambda self, hero: Hero.teleport(hero))],
                  2: [Equipment("bow", usage=lambda self, hero: Hero.throw(hero, Arrow("Arrow", 2)))],
                  3: [Equipment("portoloin", "w", usage=lambda self, hero: Hero.teleport(hero)) , Equipment("Nunchaku", "^", usage=lambda self, hero: Hero.setStrength(8))], }
    """ available monsters """
    monsters = {0: [Creature("Goblin", 4), Creature("Bat", 2, "W")],
                1: [Creature("Ork", 6, strength=2), Creature("Blob", 10)], 5: [Creature("Dragon", 20, strength=3)],
                6: [Creature("Spider", 20, "S", strength=2)]}

    """ available actions """
    _actions = {'z': lambda h: theGame()._floor.move(h, Coord(0, -1)),
                'q': lambda h: theGame()._floor.move(h, Coord(-1, 0)),
                's': lambda h: theGame()._floor.move(h, Coord(0, 1)),
                'd': lambda h: theGame()._floor.move(h, Coord(1, 0)),
                'x': lambda h: theGame()._floor.move(h, Coord(1, 1)),
                'w': lambda h: theGame()._floor.move(h, Coord(-1, 1)),
                'e': lambda h: theGame()._floor.move(h, Coord(1, -1)),
                'a': lambda h: theGame()._floor.move(h, Coord(-1, -1)),
                'i': lambda h: theGame().addMessage(h.fullDescription()),
                'k': lambda h: h.__setattr__('hp', 0),
                'u': lambda h: h.use(theGame().select(h._inventory)),
                ' ': lambda h: None,
                'p': lambda h: h.useMagic(theGame().selectMagie(h.getSorts())),
                'h': lambda hero: theGame().addMessage("Actions disponibles : " + str(list(Game._actions.keys()))),
                'b': lambda hero: theGame().addMessage("I am " + hero.name),
                'c': lambda hero: theGame().destroyEquipment()}

    def __init__(self, level=1, hero=None):
        self._level = level
        self._messages = []
        if hero == None:
            hero = Hero()
        self._hero = hero
        self._floor = None

    def buildFloor(self):
        """Creates a map for the current floor."""
        self._floor = Map(hero=self._hero)
        self._floor.put(self._floor._rooms[-1].center(), Stairs())
        self._level += 1

    def getFloor(self):
        return self._floor

    def addMessage(self, msg):
        """Adds a message in the message list."""
        self._messages.append(msg)

    def destroyEquipment(self):
        """" Destroy a piece of equipment"""
        if self._hero._inventory == []:
            return
        self._hero._inventory.pop(0)

    def readMessages(self):
        """Returns the message list and clears it."""
        s = ''
        for m in self._messages:
            s += m + '. '
        self._messages.clear()
        return s

    def randElement(self, collect):
        """Returns a clone of random element from a collection using exponential random law."""
        x = random.expovariate(1 / self._level)
        for k in collect.keys():
            if k <= x:
                l = collect[k]
        return copy.copy(random.choice(l))

    def randEquipment(self):
        """Returns a random equipment."""
        return self.randElement(Game.equipments)

    def randMonster(self):
        """Returns a random monster."""
        return self.randElement(Game.monsters)

    def select(self, l):
        print("Choose item> " + str([str(l.index(e)) + ": " + e.name for e in l]))
        c = getch()
        if c.isdigit() and int(c) in range(len(l)):
            return l[int(c)]

    def selectMagie(self, l):
        print("Choose a sort> " + str([str(l.index(e)) + ": " + e[1] for e in l]))
        c = getch()
        if c.isdigit() and int(c) in range(len(l)):
            print(l[int(c)][0])
            return l[int(c)][0]

    def play(self):
        """Main game loop"""
        self.buildFloor()
        print("--- Welcome Hero! ---")
        self.equipments.get(2)[0].meet(self._hero)
        while self._hero.hp > 0:
            print()
            print(self._floor)
            print(self._hero.description())
            print(self.readMessages())
            c = getch()
            if c in Game._actions:
                Game._actions[c](self._hero)
            self._floor.moveAllMonsters()
        print("--- Game Over ---")


def theGame(game=Game()):
    """Game singleton"""
    return game


getch = _find_getch()
theGame().play()
