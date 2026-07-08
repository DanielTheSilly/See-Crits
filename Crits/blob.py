from base import Critter, enum
import random

class Blob(Critter):

    rand = random.Random()
    
    def __init__(self):
        self.anger = 0
        self.symbol = 'o'
    
    def move(self, forward, left, right, back):
        choice = self.rand.randint(0, self.anger)
        match choice:
            case 0:
                self.anger = self.anger + 1
                return enum.WAIT
            case 1:
                return enum.LEFT
            case 2:
                return enum.RIGHT
            case _:
                return enum.FORWARD
        return 0
