import pyvisa
import time
from threading import Thread
from tkinter import *



def start_loop():
    global stop
    global temp_array
    global time_array
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
    temp_array = []
    time_array = []
    while  stop:
        DMM.write(':SENS:FUNC:OFF:ALL')
        temp = round((float(DMM.query(':READ?').strip())), 3)
        print(templabel+str(num)+": "+str(temp))
        temp_array.append(temp)
        elapsed_time = round((time.time() - start_time), 3)
        print(timelabel+str(num)+": "+str(elapsed_time))
        time_array.append(elapsed_time)
        num = num + 1
        time.sleep(0.5)
    
def end_loop():
    global stop
    global temp_array
    global time_array
    print(temp_array)
    print(time_array)
    stop = False
            

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