import pyvisa
from threading import Thread
from tkinter import *
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np


def start_loop():
    global run
    run = True
    if run:
        rm = pyvisa.ResourceManager()
        print(rm)
        rm_id = pyvisa.ResourceManager().list_resources()
        print(rm_id)
        DMM = rm.open_resource('USB0::0x05E6::0x2110::1423039::INSTR')
        #DMM data retrieval
        def get_dmm_data():
            DMM.write(':SENS:FUNC:OFF:ALL')
            temp = round((float(DMM.query(':READ?').strip())), 3)
            return temp

        # Initialize variables for the plot
        x_data = []
        y_data = []

        # Set up the figure and axis
        fig, ax = plt.subplots()
        line, = ax.plot([], [], lw=1)

        # Set the axis limits
        ax.set_xlim(0, 50)
        ax.set_ylim(-25, 50)

        # Update function for the animation
        def update(frame):
            # Get data from DMM
            y = get_dmm_data()

            # Append data to lists
            x_data.append(frame)
            y_data.append(y)

            # Update the line data
            line.set_data(x_data, y_data)

            return line,

    # Create the animation
    ani = FuncAnimation(fig, update, frames=range(100), blit=True, interval=500)

    # Show the plot
    plt.show()

    
def end_loop():
    global run
    run = False
    plt.close()



temprecord = Tk()
temprecord.geometry("600x500")
temprecord.title("Test Start and End Panel")

startbtn = Button(temprecord,
                     text="Start Recording",
                     font=("Comic Sans", 30),
                     fg="#00FF00",
                     activeforeground="#00FF00",
                     bg="black",
                     activebackground="black",
                     command=lambda: Thread(target=start_loop).start())
startbtn.pack(side="left")

endbtn = Button(temprecord,
                     text="End Recording",
                     font=("Comic Sans", 30),
                     fg="#FF0000",
                     activeforeground="#FF0000",
                     bg="black",
                     activebackground="black",
                     command=end_loop)
endbtn.pack(side="right")

temprecord.mainloop()