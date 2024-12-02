import pandas as pd
import matplotlib.pyplot as plt
from ursina import *
import numpy as np
import os

class Stopwatch(Entity):
    def __init__(user, **kwargs):
        super().__init__(**kwargs)
        user.timeElapsed = 0  
        user.running = False
        user.textEntity = Text(text="000:00:00.00", color=color.white, font='VeraMono.ttf', position=(-0.35, -.16), origin=(0, 0), enabled=False)

    def update(user):
        if user.running:
            speed_factor = 20  # Speed up the stopwatch (20x speed)
            user.timeElapsed += time.dt * speed_factor  # Multiply time by speed factor to speed up the stopwatch
            hours = int(user.timeElapsed // 3600)
            minutes = int((user.timeElapsed % 3600) // 60)
            seconds = int(user.timeElapsed % 60)
            milliseconds = int((user.timeElapsed % 1) * 1000)  
            clockappFormat = f"{hours:03}:{minutes:02}:{seconds:02}.{milliseconds:02}"
            user.textEntity.text = clockappFormat

    def start(user):
        user.running = True

    def stop(user):
        user.running = False

    def reset(user):
        user.timeElapsed = 0
        user.textEntity.text = "000:00:00.00"

app = Ursina()
stopwatch = Stopwatch()

def start_stopwatch():
    stopwatch.start()

def stop_stopwatch():
    stopwatch.stop()

def reset_stopwatch():
    stopwatch.reset()

circle = Entity(model='circle', color=color.red, scale=(.9, .8, .8), position=(.09, -3.2), collider="box")

drawing_entity = Entity(model='quad', texture='drawing.png', scale=(14.6, 8), position=(0, -.08), enabled=False)

buttons_created = False

graph_entity = Entity(model='quad', scale=(1.2, 1, 1), position=(3.64, -1.64), texture=None, enabled=False, collider='box')
graph_entity.expanded = False

# Initialize buttons and logo outside of the circle click
startButton = Button(text="Start", color=color.green, position=(-0.15, -0.15), scale=(.04, .04), on_click=start_stopwatch, enabled=False)
stopButton = Button(text="Stop", color=color.red, position=(-0.15, -0.2), scale=(0.04, 0.04), on_click=stop_stopwatch, enabled=False)
resetButton = Button(text="Reset", color=color.blue, position=(-0.15, -0.25), scale=(0.04, 0.04), on_click=reset_stopwatch, enabled=False)
logo_entity = Entity(model='quad', texture='logo.png', scale=(1.5, 1, 1), position=(.007, -1.5), enabled=False)
startButton.text_entity.scale = (14, 14)
stopButton.text_entity.scale = (14, 14)
resetButton.text_entity.scale = (14, 14)

def toggle_graph_size():
    if graph_entity.expanded:
        graph_entity.scale = (1.2, 1, 1)
        graph_entity.position = (3.64, -1.64)
    else:
        graph_entity.scale = (6, 4, 4)
        graph_entity.position = (0, 0)
    graph_entity.expanded = not graph_entity.expanded

graph_entity.on_click = toggle_graph_size

def on_circle_click():
    global buttons_created
    drawing_entity.enabled = not drawing_entity.enabled
    graph_entity.enabled = drawing_entity.enabled
    if drawing_entity.enabled:
        stopwatch.textEntity.enabled = True
        startButton.enabled = True
        stopButton.enabled = True
        resetButton.enabled = True
        logo_entity.enabled = True
        speedometer.enabled=True
        speed_label.enabled=True
        direction_spinner.enabled = True
    else:
        stopwatch.textEntity.enabled = False
        graph_entity.enabled = False
        logo_entity.enabled = False
        startButton.enabled = False
        stopButton.enabled = False
        resetButton.enabled = False
        speedometer.enabled=False
        speed_label.enabled = False
        direction_spinner.enabled = False
circle.on_click = on_circle_click

# Step 1: Read CSV file with velocity data
df = pd.read_csv('data.csv')

time_data = df['MISSION ELAPSED TIME (min)'] * 60
x_velocity = df['Vx(km/s)[J2000-EARTH]']
y_velocity = df['Vy(km/s)[J2000-EARTH]']
z_velocity = df['Vz(km/s)[J2000-EARTH]']
speed_data = np.sqrt(x_velocity**2 + y_velocity**2 + z_velocity**2)

current_index = 0

def plot_velocity_at_time(elapsed_time):
    global current_index

    if elapsed_time >= 480 and current_index < len(time_data):
        elapsed_times = []
        x_vals, y_vals, z_vals = [], [], []

        while current_index < len(time_data) and time_data[current_index] <= elapsed_time:
            elapsed_times.append(time_data[current_index])
            x_vals.append(x_velocity[current_index])
            y_vals.append(y_velocity[current_index])
            z_vals.append(z_velocity[current_index])
            current_index += 1

        plt.figure(figsize=(8, 6))
        plt.plot(elapsed_times, x_vals, label="X Velocity", color='r')
        plt.plot(elapsed_times, y_vals, label="Y Velocity", color='g')
        plt.plot(elapsed_times, z_vals, label="Z Velocity", color='b')

        plt.title('Velocity Over Time')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Velocity (km/s)')
        plt.legend()

        plot_path = 'velocity_plot.png'
        plt.savefig(plot_path, dpi=300)
        plt.close()

        if os.path.exists(plot_path):
            texture = Texture(plot_path)
            graph_entity.texture = texture
            graph_entity.enabled = True

# Speedometer setup
speedometer = Entity(model='circle', scale=.85, color=color.black, position=(2.15, -1.60), enabled=False)
speedometer_needle = Entity(parent=speedometer, model='quad', scale=(0.1, .6), color=color.red, position=(0, 0), origin=(0, -0.5))
speed_label = Text(text="0 km/s", position=(.26,-.263), color=color.white, origin=(0,0), enabled=False)

def update_speedometer(elapsed_time):
    idx = np.searchsorted(time_data, elapsed_time, side='right') - 1
    if 0 <= idx < len(speed_data):
        speed = speed_data[idx]
        max_speed = 10
        speed_fraction = min(speed / max_speed, 1)

        angle = lerp(-90, 90, speed_fraction)
        speedometer_needle.rotation_z = angle

        speed_label.text = f"{speed:.2f} km/s"


time_data = df['MISSION ELAPSED TIME (min)'] * 60  # Convert minutes to seconds
rx_data = df['Rx(km)[J2000-EARTH]']
ry_data = df['Ry(km)[J2000-EARTH]']

# Spinner setup (add Earth representation)
direction_spinner = Entity(model='circle', scale=0.5, color=color.azure, position=(-2.8, -2), enabled=False)
earth_representation = Entity(parent=direction_spinner, model='circle', scale=0.2, color=color.green)  # Represent Earth
spinner_needle = Entity(parent=direction_spinner, model='quad', scale=(0.02, 0.4), color=color.yellow, position=(0, 0), origin=(0, -0.5))

# Update function
def update_direction_spinner(elapsed_time):
    idx = np.searchsorted(time_data, elapsed_time, side='right') - 1
    if 0 <= idx < len(time_data):
        rx = rx_data.iloc[idx]
        ry = ry_data.iloc[idx]

        # Calculate angle (atan2 ensures correct quadrant)
        angle = np.degrees(np.arctan2(ry, rx))
        
        # Normalize position for Earth scale visualization (optional)
        r_max = 6371  # Earth's approximate radius in km
        norm_rx = rx / r_max
        norm_ry = ry / r_max

        # Update needle rotation
        spinner_needle.rotation_z = -angle

def update():
    if stopwatch.running:
        elapsed_time = stopwatch.timeElapsed
        plot_velocity_at_time(elapsed_time)
        update_speedometer(elapsed_time)
        update_direction_spinner(elapsed_time)

app.run()
