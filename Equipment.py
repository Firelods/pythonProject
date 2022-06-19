from Element import Element

# from main import theGame
# from Game import Game


class Equipment(Element):
    """A piece of equipment"""

    def __init__(self, name, abbrv="", usage=None):
        Element.__init__(self, name, abbrv)
        self.usage = usage

    def meet(self, hero):
        """Makes the hero meet an element. The hero takes the element."""
        hero.take(self)
        # Game().addMessage("You pick up a " + self.name)
        return True

    def use(self, creature):
        """Uses the piece of equipment. Has effect on the hero according usage.
            Return True if the object is consumed."""
        if self.usage is None:
            # Game().addMessage("The " + self.name + " is not usable")
            return False
        else:
            # Game().addMessage("The " + creature.name + " uses the " + self.name)
            return self.usage(self, creature)
