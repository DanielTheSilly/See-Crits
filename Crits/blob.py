from base import Critter, enum
import random

# The name of the class will need to be changed for your critters.
class Blob(Critter):

    # This random object is shared between all Blobs for efficiency.
    rand = random.Random()
    
    def __init__(self):
        # Blobs start out calm.
        self.anger = 0
        # The symbol is needed to tell the program what to display.
        self.symbol = 'o'
    
    def move(self, forward, left, right, back):
        choice = self.rand.randint(0, self.anger)
        # choice is now a random number from 0 to however much anger the blob has.
        match choice:
            case 0:
                # In case of a zero, anger increases, but the Blob waits.
                self.anger = self.anger + 1
                return enum.WAIT
            case 1:
                return enum.LEFT
            case 2:
                # In case of a 1 or 2 the Blob will turn.
                return enum.RIGHT
            case _:
                # For all other cases, the Blob will be aggressive.
                if left == enum.ENEMY:
                    # If an enemy is seen on tje left, the Blob will turn to it.
                    return enun.RIGHT
                # The Blob tries to move forward!
                return enum.FORWARD
        # In case something has gone wrong, the code returns a 0 to ensure there is not a crash.
        return 0
