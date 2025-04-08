import tkinter as tk
from constants import *
from PIL import Image, ImageTk  # Pillow for image processing

class Vehicle:
    def __init__(self, canvas, direction, intersection_x, intersection_y):
        self.canvas = canvas
        self.direction = direction
        self.intersection_x = intersection_x
        self.intersection_y = intersection_y
        self.speed = VEHICLE_SPEED
        self.moving = True
        self.stopped = False
        self.image = None
        self.image_id = None
        self.tk_image = None
        self.load_image()
        self.create_vehicle()

    def load_image(self):
        img_path = ""
        if self.direction == NORTH:
            img_path = "car_north.png"
        elif self.direction == SOUTH:
            img_path = "car_south.png"
        elif self.direction == EAST:
            img_path = "car_east.png"
        elif self.direction == WEST:
            img_path = "car_west.png"

        # Resize image to fit lane
        original = Image.open(img_path)
        resized = original.resize((30, 50)) if self.direction in [NORTH, SOUTH] else original.resize((50, 30))
        self.tk_image = ImageTk.PhotoImage(resized)

    def create_vehicle(self):
        if self.direction == NORTH:
            self.x = self.intersection_x - LANE_WIDTH // 2
            self.y = self.intersection_y + 250
        elif self.direction == SOUTH:
            self.x = self.intersection_x + LANE_WIDTH // 2
            self.y = self.intersection_y - 250
        elif self.direction == EAST:
            # Fix: Adjust the starting position for East vehicles to come from the left
            self.x = self.intersection_x - 250
            self.y = self.intersection_y - LANE_WIDTH // 2
        elif self.direction == WEST:
            # Fix: Adjust the starting position for West vehicles to come from the right
            self.x = self.intersection_x + 250
            self.y = self.intersection_y + LANE_WIDTH // 2

        self.image_id = self.canvas.create_image(self.x, self.y, image=self.tk_image, anchor=tk.CENTER)

    def move(self, traffic_lights, vehicles):
        # Get the current light state for the vehicle's direction
        light = traffic_lights[self.direction]
        
        # Find the closest vehicle in the same direction
        lead_vehicle = None
        min_gap = float('inf')
        for vehicle in vehicles:
            if vehicle != self and vehicle.direction == self.direction:
                if self.direction == NORTH and vehicle.y < self.y:
                    gap = self.y - vehicle.y
                    if gap < min_gap:
                        min_gap = gap
                        lead_vehicle = vehicle
                elif self.direction == SOUTH and vehicle.y > self.y:
                    gap = vehicle.y - self.y
                    if gap < min_gap:
                        min_gap = gap
                        lead_vehicle = vehicle
                elif self.direction == EAST and vehicle.x > self.x:
                    gap = vehicle.x - self.x
                    if gap < min_gap:
                        min_gap = gap
                        lead_vehicle = vehicle
                elif self.direction == WEST and vehicle.x < self.x:
                    gap = self.x - vehicle.x
                    if gap < min_gap:
                        min_gap = gap
                        lead_vehicle = vehicle

        # Check if the vehicle is approaching the intersection
        approaching = False
        if self.direction == NORTH and 0 < self.y - self.intersection_y < 70:
            approaching = True
        elif self.direction == SOUTH and 0 < self.intersection_y - self.y < 70:
            approaching = True
        elif self.direction == EAST and 0 < self.intersection_x - self.x < 70:
            approaching = True
        elif self.direction == WEST and 0 < self.x - self.intersection_x < 70:
            approaching = True

        # Check if the vehicle has passed the intersection
        passed_intersection = (
            (self.direction == NORTH and self.y < self.intersection_y) or
            (self.direction == SOUTH and self.y > self.intersection_y) or
            (self.direction == EAST and self.x > self.intersection_x) or
            (self.direction == WEST and self.x < self.intersection_x)
        )

        # Stop the vehicle if the light is red, or it's too close to another vehicle
        if (approaching and light.state in ["red", "yellow"] and not passed_intersection) or \
        (lead_vehicle and min_gap < MIN_VEHICLE_GAP + VEHICLE_LENGTH):
            self.moving = False
            self.stopped = True
        else:
            self.moving = True
            self.stopped = False

        # Move the vehicle if it's allowed
        if self.moving:
            dx, dy = 0, 0
            if self.direction == NORTH:
                dy = -self.speed
                self.y += dy
            elif self.direction == SOUTH:
                dy = self.speed
                self.y += dy
            elif self.direction == EAST:
                dx = self.speed
                self.x += dx
            elif self.direction == WEST:
                dx = -self.speed
                self.x += dx
            self.canvas.move(self.image_id, dx, dy)

        # Remove vehicle when it moves off-screen
        if (self.direction == NORTH and self.y < -50) or \
        (self.direction == SOUTH and self.y > self.canvas.winfo_height() + 50) or \
        (self.direction == EAST and self.x > self.canvas.winfo_width() + 50) or \
        (self.direction == WEST and self.x < -50):
            self.canvas.delete(self.image_id)
            return True

        return False
