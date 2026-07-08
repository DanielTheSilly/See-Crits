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
        pass
        # TODO Update grid logic here
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
            if j >= len(self.critList):
                j = 0

window = ZooWindow()
window.populate()
# Populate with dummy data: (grid_x, grid_y, symbol)
# window.critters = [(2, 2, 'A'), (5, 8, 'B')] 
arcade.run()
