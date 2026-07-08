import arcade
import importlib
import pkgutil
import inspect
import Crits
import random
from base import Critter, enum

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TILE_SIZE = 20
FONT_SIZE = int(TILE_SIZE*0.8)

class ZooWindow(arcade.Window):

    rand = random.Random()
        
    def load_crits(self):
        found_crits = []
        
        for loader, modual_name, is_pkg in pkgutil.iter_modules(["Crits"]):
            module = importlib.import_module(f"Crits.{modual_name}")
            
            for name,obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Critter) and obj is not Critter:
                     found_crits.append(obj)
                     print(f"loaded critter: {name}")
        
        return found_crits

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "See Crits")
        self.critters = [[None for _ in range(int(SCREEN_HEIGHT / TILE_SIZE))] for _ in range(int(SCREEN_WIDTH / TILE_SIZE))]
        self.facing = [[1 for _ in range(int(SCREEN_HEIGHT / TILE_SIZE))] for _ in range(int(SCREEN_WIDTH / TILE_SIZE))]
        self.is_running = False
        self.critList = self.load_crits()

    def on_draw(self):
        # 1. Clear the screen (this replaces start_render)
        self.clear()

        # Draw your grid lines
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            arcade.draw_line(x, 0, x, SCREEN_HEIGHT, arcade.color.GRAY, 1)
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            arcade.draw_line(0, y, SCREEN_WIDTH, y, arcade.color.GRAY, 1)
            
        # Draw your characters
        for x, row in enumerate(self.critters):
            for y, critter in enumerate(row):
                if critter != None:
                    text_x = (x * TILE_SIZE) + (TILE_SIZE / 2) - (FONT_SIZE / 2)
                    text_y = (y * TILE_SIZE) + (TILE_SIZE / 2) - (FONT_SIZE / 2)
                    symbol = critter.symbol
                    arcade.draw_text(symbol, text_x, text_y, arcade.color.WHITE, FONT_SIZE)
        #for (x, y, symbol) in self.critters:
            #text_x = (x * TILE_SIZE) + (TILE_SIZE / 2) - (FONT_SIZE / 2)
            #text_y = (y * TILE_SIZE) + (TILE_SIZE / 2) - (FONT_SIZE / 2)
            #arcade.draw_text(symbol, text_x, text_y, arcade.color.WHITE, FONT_SIZE)
                             
        # Draw UI status
        status = "RUNNING" if self.is_running else "PAUSED"
        arcade.draw_text(f"Status: {status} (Space: Play/Pause, Enter: Step)", 
                         10, 570, arcade.color.GREEN, 14)

    def on_update(self, delta_time):
        if self.is_running:
            self.tick_simulation()
            
    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.is_running = not self.is_running
        elif key == arcade.key.ENTER:
            self.tick_simulation()

    def tick_simulation(self):
        # Generate all possible coordinate pairs (x, y)
        coords = [(x, y) for x in range(len(self.critters)) for y in range(len(self.critters[x]))]

        # Shuffle the list of coordinates in-place
        random.shuffle(coords)

        # Iterate in random order
        for x, y in coords:
            critter = self.critters[x][y]
            face = self.facing[x][y]
            # Get local view for cirt
            if critter != None:
                if x == 0:
                    west = enum.WALL
                else:
                    ocritter = self.critters[x-1][y]
                    if ocritter == None:
                        west = enum.EMPTY
                    else:
                        if type(ocritter) == type(critter):
                            west = enum.FRIEND
                        else:
                            west = enum.ENEMY
                if x == len(self.critters)-1:
                    east = enum.WALL
                else:
                    ocritter = self.critters[x+1][y]
                    if ocritter == None:
                        east = enum.EMPTY
                    else:
                        if type(ocritter) == type(critter):
                            east = enum.FRIEND
                        else:
                            east = enum.ENEMY
                if y == 0:
                    north = enum.WALL
                else:
                    ocritter = self.critters[x][y-1]
                    if ocritter == None:
                        north = enum.EMPTY
                    else:
                        if type(ocritter) == type(critter):
                            north = enum.FRIEND
                        else:
                            north = enum.ENEMY
                if y == len(self.critters[x])-1:
                    south = enum.WALL
                else:
                    ocritter = self.critters[x][y+1]
                    if ocritter == None:
                        south = enum.EMPTY
                    else:
                        if type(ocritter) == type(critter):
                            south = enum.FRIEND
                        else:
                            south = enum.ENEMY
                # Get move
                # TODO name the numbes in facing with enums
                if face == 0:
                    move = critter.move(north, west, east, south)
                elif face == 1:
                    move = critter.move(east, north, south, west)
                elif face == 2:
                    move = critter.move(south, east, west, north)
                else: # elif face == 3:
                    move = critter.move(west, south, north, east)
                # Update grid
                if move == enum.WAIT:
                    pass
                elif move == enum.LEFT:
                    face = face -1
                    if face == -1:
                        face = 3
                    pass
                elif move == enum.RIGHT:
                    face = face +1
                    if face == 4:
                        face = 0
                    pass
                elif move == enum.FORWARD:
                    if face == 0:
                        if north == enum.WALL or north == enum.FRIEND:
                            pass
                        elif north == enum.ENEMY:
                            self.critters[x][y-1] = type(critter)()
                            pass
                        elif north == enum.EMPTY:
                            self.critters[x][y] = None
                            self.critters[x][y-1] = critter
                            pass
                    elif face == 1:
                        if east == enum.WALL or east == enum.FRIEND:
                            pass
                        elif east == enum.ENEMY:
                            self.critters[x][y-1] = type(critter)()
                            pass
                        elif east == enum.EMPTY:
                            self.critters[x][y] = None
                            self.critters[x][y-1] = critter
                            pass
                    elif face == 2:
                        if south == enum.WALL or south == enum.FRIEND:
                            pass
                        elif south == enum.ENEMY:
                            self.critters[x][y-1] = type(critter)()
                            pass
                        elif south == enum.EMPTY:
                            self.critters[x][y] = None
                            self.critters[x][y-1] = critter
                            pass
                    else:
                        if west == enum.WALL or west == enum.FRIEND:
                            pass
                        elif west == enum.ENEMY:
                            self.critters[x][y-1] = type(critter)()
                            pass
                        elif west == enum.EMPTY:
                            self.critters[x][y] = None
                            self.critters[x][y-1] = critter
                            pass
        # print("Ticking one step...")
    
    def populate(self):
        j = 0
        i = (SCREEN_WIDTH / TILE_SIZE) * (SCREEN_HEIGHT / TILE_SIZE) / 4
        while i > 0:
            #print(f"i = {i}")
            i = i - 1
            x = self.rand.randint(0, len(self.critters)-1)
            #print(f"x = {x}")
            #print(f"self.critters[x] = {self.critters[x]}")
            y = self.rand.randint(0, len(self.critters[x])-1)
            #print(f"self.critters[x][y] = {self.critters[x][y]}")
            while self.critters[x][y] != None:
                x = self.rand.randint(0, len(self.critters)-1)
                y = self.rand.randint(0, len(self.critters[x])-1)
            self.critters[x][y] = self.critList[j]()
            self.facing[x][y] = self.rand.randint(0,3)
            if j >= len(self.critList):
                j = 0

window = ZooWindow()
window.populate()
# Populate with dummy data: (grid_x, grid_y, symbol)
# window.critters = [(2, 2, 'A'), (5, 8, 'B')] 
arcade.run()
