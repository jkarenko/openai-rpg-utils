import random

class Dice:
    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)

class DnDDice:
    def __init__(self):
        self.d4 = Dice(4)
        self.d6 = Dice(6)
        self.d8 = Dice(8)
        self.d10 = Dice(10)
        self.d12 = Dice(12)
        self.d20 = Dice(20)

    def roll(self, dice):
        return dice.roll()
