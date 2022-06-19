from Creature import Creature
from Equipment import Equipment


class Hero(Creature):
    """The hero of the game.
        Is a creature. Has an inventory of elements. """

    def __init__(self, name="Hero", hp=10, abbrv="@", strength=2):
        Creature.__init__(self, name, hp, abbrv, strength)
        self._inventory = []
        self._or = 0

    def description(self):
        """Description of the hero"""
        return Creature.description(self) + str(self._inventory) + str(self._or)

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
        if elem.abbrv != "o":
            if len(self._inventory) < 10:
                self._inventory.append(elem)

        else:
            self._or += 1

    def use(self, elem):
        """Use a piece of equipment"""
        if elem is None:
            return
        self.checkEquipment(elem)
        if elem not in self._inventory:
            raise ValueError('Equipment ' + elem.name + 'not in inventory')
        if elem.use(self):
            self._inventory.remove(elem)

    def heal(self, hp):
        """Heal the hero"""
        self.hp += hp


