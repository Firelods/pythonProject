import copy
import math
import random
import tkinter
import Game
import Room


# exceptions


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


def heal(creature):
    """Heal the creature"""
    creature.hp += 3
    return True


def teleport(creature, unique):
    """Teleport the creature"""
    r = theGame()._floor.randRoom()
    c = r.randCoord()
    theGame()._floor.rm(theGame()._floor.pos(creature))
    theGame()._floor.put(c, creature)
    return unique


def theGame(game=Game):
    """Game singleton"""
    return game


getch = _find_getch()
theGame().play()
