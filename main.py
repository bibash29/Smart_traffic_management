import tkinter as tk
from tkinter import ttk, messagebox
from traffic_light import TrafficLight
from vehicle import Vehicle
from intersection import IntersectionController
from constants import *
import random
import time

# -----------------------------
# Login window function
# -----------------------------
def show_login():
    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        if username == "bibash" and password == "bibash":
            login_window.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    login_window = tk.Tk()
    login_window.title("Traffic Controller Login")
    login_window.geometry("300x180")
    login_window.resizable(False, False)

    tk.Label(login_window, text="Username:").pack(pady=(20, 5))
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password:").pack(pady=(10, 5))
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    tk.Button(login_window, text="Login", command=attempt_login).pack(pady=15)

    login_window.mainloop()

# -----------------------------
# Main simulation class
# -----------------------------
class TrafficSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Traffic Management System")

        self.canvas = tk.Canvas(root, width=600, height=600, bg=DARK_GREEN)
        self.canvas.pack()

        self.intersection_x = 300
        self.intersection_y = 300

        self.draw_roads()

        self.traffic_lights = [
            TrafficLight(self.canvas, self.intersection_x, self.intersection_y, NORTH),
            TrafficLight(self.canvas, self.intersection_x, self.intersection_y, EAST),
            TrafficLight(self.canvas, self.intersection_x, self.intersection_y, SOUTH),
            TrafficLight(self.canvas, self.intersection_x, self.intersection_y, WEST)
        ]

        self.controller = IntersectionController(self.traffic_lights)

        self.vehicles = []
        self.last_vehicle_time = time.time()

        self.create_control_panel()

        self.running = True
        self.update()

    def draw_roads(self):
        # North-South road
        self.canvas.create_rectangle(
            self.intersection_x - LANE_WIDTH - ROAD_WIDTH // 2, 0,
            self.intersection_x - LANE_WIDTH + ROAD_WIDTH // 2, 600,
            fill=GRAY, outline=BLACK
        )
        self.canvas.create_rectangle(
            self.intersection_x + LANE_WIDTH - ROAD_WIDTH // 2, 0,
            self.intersection_x + LANE_WIDTH + ROAD_WIDTH // 2, 600,
            fill=GRAY, outline=BLACK
        )

        # East-West road
        self.canvas.create_rectangle(
            0, self.intersection_y - LANE_WIDTH - ROAD_WIDTH // 2,
            600, self.intersection_y - LANE_WIDTH + ROAD_WIDTH // 2,
            fill=GRAY, outline=BLACK
        )
        self.canvas.create_rectangle(
            0, self.intersection_y + LANE_WIDTH - ROAD_WIDTH // 2,
            600, self.intersection_y + LANE_WIDTH + ROAD_WIDTH // 2,
            fill=GRAY, outline=BLACK
        )

        # Intersection center
        self.canvas.create_rectangle(
            self.intersection_x - INTERSECTION_SIZE // 2,
            self.intersection_y - INTERSECTION_SIZE // 2,
            self.intersection_x + INTERSECTION_SIZE // 2,
            self.intersection_y + INTERSECTION_SIZE // 2,
            fill=GRAY, outline=BLACK
        )

        self.canvas.create_line(self.intersection_x, 0, self.intersection_x, 600, fill=WHITE, width=2)
        self.canvas.create_line(0, self.intersection_y, 600, self.intersection_y, fill=WHITE, width=2)

    def create_control_panel(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        self.mode_var = tk.StringVar(value="Auto")
        ttk.Radiobutton(control_frame, text="Auto Mode", variable=self.mode_var,
                        value="Auto", command=self.set_auto_mode).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(control_frame, text="Manual Mode", variable=self.mode_var,
                        value="Manual", command=self.set_manual_mode).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Switch Lights", command=self.manual_switch).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Exit", command=self.exit_app).pack(side=tk.RIGHT, padx=5)

    def set_auto_mode(self):
        self.controller.set_mode("auto")

    def set_manual_mode(self):
        self.controller.set_mode("manual")

    def manual_switch(self):
        if self.controller.mode == "manual":
            self.controller.manual_switch()

    def exit_app(self):
        self.running = False
        self.root.destroy()

    def spawn_vehicle(self):
        current_time = time.time()
        if current_time - self.last_vehicle_time > VEHICLE_SPAWN_RATE / 1000:
            direction = random.choice([NORTH, SOUTH, EAST, WEST])
            self.vehicles.append(Vehicle(
                self.canvas, direction,
                self.intersection_x, self.intersection_y
            ))
            self.last_vehicle_time = current_time

    def update(self):
        if not self.running:
            return

        if self.controller.mode == "auto":
            self.controller.update_auto()

        self.spawn_vehicle()

        vehicles_to_remove = []
        for i, vehicle in enumerate(self.vehicles):
            should_remove = vehicle.move(self.traffic_lights, self.vehicles)
            if should_remove:
                vehicles_to_remove.append(i)

        for i in sorted(vehicles_to_remove, reverse=True):
            if i < len(self.vehicles):
                self.vehicles.pop(i)

        self.root.after(30, self.update)

# -----------------------------
# App Entry Point
# -----------------------------
if __name__ == "__main__":
    show_login()  # Show login window first
    root = tk.Tk()
    app = TrafficSimulation(root)
    root.protocol("WM_DELETE_WINDOW", app.exit_app)
    root.mainloop()
