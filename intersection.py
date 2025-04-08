from constants import *
import time

class IntersectionController:
    def __init__(self, traffic_lights):
        self.traffic_lights = traffic_lights
        self.mode = "auto"
        self.current_green = NORTH
        self.next_change_time = 0
        self.set_initial_state()
        
    def set_initial_state(self):
        # Set north-south to green, east-west to red
        self.traffic_lights[NORTH].change_state("green")
        self.traffic_lights[SOUTH].change_state("green")
        self.traffic_lights[EAST].change_state("red")
        self.traffic_lights[WEST].change_state("red")
        self.current_green = NORTH
        self.next_change_time = time.time() + GREEN_DURATION / 1000
        
    def update_auto(self):
        current_time = time.time()
        if current_time >= self.next_change_time:
            if self.traffic_lights[self.current_green].state == "green":
                # Change to yellow
                self.traffic_lights[self.current_green].change_state("yellow")
                self.traffic_lights[(self.current_green + 2) % 4].change_state("yellow")
                self.next_change_time = current_time + YELLOW_DURATION / 1000
            else:
                # Change to red and switch to other direction
                self.traffic_lights[self.current_green].change_state("red")
                self.traffic_lights[(self.current_green + 2) % 4].change_state("red")
                
                # Switch to east-west or north-south
                self.current_green = EAST if self.current_green == NORTH else NORTH
                
                # Set new green lights
                self.traffic_lights[self.current_green].change_state("green")
                self.traffic_lights[(self.current_green + 2) % 4].change_state("green")
                self.next_change_time = current_time + GREEN_DURATION / 1000
                
    def manual_switch(self):
        if self.mode != "manual":
            return
            
        # Only allow switching if current lights are not yellow
        if self.traffic_lights[self.current_green].state == "yellow":
            return
            
        # Switch to the other direction
        self.traffic_lights[self.current_green].change_state("red")
        self.traffic_lights[(self.current_green + 2) % 4].change_state("red")
        
        self.current_green = EAST if self.current_green == NORTH else NORTH
        self.traffic_lights[self.current_green].change_state("green")
        self.traffic_lights[(self.current_green + 2) % 4].change_state("green")
        
    def set_mode(self, mode):
        self.mode = mode
        if mode == "auto":
            self.set_initial_state()