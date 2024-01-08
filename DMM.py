import pyvisa
import time
from threading import Thread
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np


temp_file = open('temp.txt', 'a')
time_file = open('time.txt', 'a')

def dataplot():
    x_file = 'time.txt'
    y_file = 'temp.txt'
    x_values = np.loadtxt(x_file)
    y_values = np.loadtxt(y_file)
    plt.plot(x_values, y_values)
    plt.xlabel("time(seconds)")
    plt.ylabel("temperature(C)")
    plt.title("Temperature over Time")
    plt.show()


def start_loop():
    global temp_file
    global time_file
    global stop
    stop = True
    rm = pyvisa.ResourceManager()
    print(rm)
    rm_id = pyvisa.ResourceManager().list_resources()
    print(rm_id)
    DMM = rm.open_resource('USB0::0x05E6::0x2110::1423039::INSTR')
    templabel = "temp"
    timelabel = "t"
    num = 1
    start_time = time.time()
    while stop:
        DMM.write(':SENS:FUNC:OFF:ALL')
        temp = round((float(DMM.query(':READ?').strip())), 3)
        print(templabel+str(num)+": "+str(temp))
        temp_file.write(f'{temp}\n')
        elapsed_time = round((time.time() - start_time), 3)
        print(timelabel+str(num)+": "+str(elapsed_time))
        time_file.write(f'{elapsed_time}\n')
        num = num + 1
        time.sleep(1)

    
def end_loop():
    global stop
    global temp_file
    global time_file
    stop = False
    with open('temp.txt', 'r') as temp_file, open('time.txt', 'r') as time_file:
        temp_content = temp_file.read()
        time_content = time_file.read()
        print(temp_content)
        print(time_content)
    dataplot()



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