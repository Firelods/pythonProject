import copy
import math
import random
import tkinter
# from Game import Game
# import Room


# exceptions


def sign(x):
    if x > 0:
        return 1
    return -1


def heal(creature):
    """Heal the creature"""
    creature.hp += 3
    return True

# def teleport(creature, unique):
#     """Teleport the creature"""
#     r = theGame()._floor.randRoom()
#     c = r.randCoord()
#     theGame()._floor.rm(theGame()._floor.pos(creature))
#     theGame()._floor.put(c, creature)
#     return unique


# def theGame(game=Game):
#     """Game singleton"""
#     return game

#
# getch = _find_getch()
# theGame().play()
