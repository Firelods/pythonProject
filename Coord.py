import math


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

