import tkinter as tk
from constants import *

class TrafficLight:
    def __init__(self, canvas, x, y, direction):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.direction = direction
        self.state = "red"
        self.light_objects = []
        self.create_light()
        
    def create_light(self):
        # Position lights based on direction
        if self.direction == NORTH:
            x, y = self.x, self.y - 70
        elif self.direction == EAST:
            x, y = self.x + 70, self.y
        elif self.direction == SOUTH:
            x, y = self.x, self.y + 70
        elif self.direction == WEST:
            x, y = self.x - 70, self.y
            
        # Create traffic light housing
        self.light_objects.append(self.canvas.create_rectangle(
            x - 10, y - 25,
            x + 10, y + 25,
            fill=BLACK, outline=WHITE
        ))
        
        # Create lights (initially all off)
        red_light = self.canvas.create_oval(
            x - 8, y - 20,
            x + 8, y - 8,
            fill=GRAY, outline=WHITE
        )
        yellow_light = self.canvas.create_oval(
            x - 8, y - 6,
            x + 8, y + 6,
            fill=GRAY, outline=WHITE
        )
        green_light = self.canvas.create_oval(
            x - 8, y + 8,
            x + 8, y + 20,
            fill=GRAY, outline=WHITE
        )
        
        self.light_objects.extend([red_light, yellow_light, green_light])
        
    def change_state(self, new_state):
        self.state = new_state
        self.update_lights()
        
    def update_lights(self):
        # Turn all lights off (gray)
        for i in range(1, 4):  # Skip the housing (index 0)
            self.canvas.itemconfig(self.light_objects[i], fill=GRAY)
            
        # Turn on the active light
        if self.state == "red":
            self.canvas.itemconfig(self.light_objects[1], fill=RED)
        elif self.state == "yellow":
            self.canvas.itemconfig(self.light_objects[2], fill=YELLOW)
        elif self.state == "green":
            self.canvas.itemconfig(self.light_objects[3], fill=GREEN)