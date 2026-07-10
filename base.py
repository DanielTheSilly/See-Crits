from abc import ABC, abstractmethod
from enum import IntEnum


class enum(IntEnum):
    WAIT = 0
    FORWARD = 1
    LEFT = 2
    RIGHT = 3
    WALL = 0
    ENEMY = 1
    EMPTY = 2
    FRIEND = 3

class Critter(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def move(forward, left, right, back):
        return 0
    
    #@abstractmethod
    #def getSymbol():
        #return 'A'
