import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import Button
import random

# Replace this function with your actual DMM data retrieval
def get_dmm_data():
    return random.uniform(0, 10)

# Initialize variables for the plot
x_data = []
y_data = []

# Set up the figure and axis
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

# Set the axis limits
ax.set_xlim(0, 10)
ax.set_ylim(0, 12)

# Flag to control live plotting
is_running = True

# Function to update the plot
def update_plot():
    global is_running
    while is_running:
        # Get data from DMM
        new_data = get_dmm_data()

        # Append data to lists
        x_data.append(len(x_data) + 1)
        y_data.append(new_data)

        # Update the line data
        line.set_data(x_data, y_data)

        # Redraw the figure
        fig.canvas.draw()
        fig.canvas.flush_events()

        # Pause for a short duration
        plt.pause(1)  # Adjust the duration as needed

# Tkinter setup for the start and stop buttons
def start_plotting():
    global is_running
    is_running = True
    update_plot()

def stop_plotting():
    global is_running
    is_running = False

root = tk.Tk()

# Create buttons to start and stop the live plot
start_button = Button(root, text="Start", command=start_plotting)
start_button.pack()

stop_button = Button(root, text="Stop", command=stop_plotting)
stop_button.pack()

# Show the plot
plt.show()

# Start the Tkinter main loop
root.mainloop()
