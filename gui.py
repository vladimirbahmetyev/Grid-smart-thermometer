import tkinter as tk
from tkinter.messagebox import showinfo
from ttk import Combobox
from PIL import ImageTk, Image
from tkinter import filedialog
from go import *

def thermometer(ArduinoSerial):
    lbl_th = tk.Label(text='')
    check = str(ArduinoSerial.readline()) 
    a = str(b'1\r\n')
    b = str(b'2\r\n')
    c = str(b'3\r\n')
    d = str(b'4\r\n')
    while (check != a):
        check = str(ArduinoSerial.readline())
        print(check)

        if (check == b):
            lbl_th.destroy()
            lbl_th = tk.Label(text='Move your hand to the sensor')
            lbl_th.place(x=25,y=75)
        if (check == c):
            lbl_th.destroy()
            lbl_th = tk.Label(text='Temperature is normal, come through')
            lbl_th.place(x=25,y=75)
        if (check == d):
            lbl_th.destroy()
            lbl_th = tk.Label(text='No passage, high temperature')
            lbl_th.place(x=25,y=75)
        
        root.update()

def detection():
    for widget in root.winfo_children():
        widget.destroy()
    ArduinoSerial = serial.Serial('com3', 9600)  # create an object to work with a serial communication port
    time.sleep(2)  # wait 2 seconds for serial communication to be established
    camera_stream = VideoStream(src=0).start()
    lbl = tk.Label(text='')
    while True:
        lbl.destroy()
        is_person_detected = check_person(camera_stream)
        if is_person_detected == '1':
            ArduinoSerial.write(is_person_detected.encode())  # pass 1
            lbl = tk.Label(text='Human Detected')
            lbl.place(x=25,y=25)
            thermometer(ArduinoSerial)
            
        else:
            lbl = tk.Label(text='Human Not Detected')
            lbl.place(x=25,y=25)
            ArduinoSerial.write(is_person_detected.encode())  # pass 0
         
        root.update()
        time.sleep(1)


def start():
    global root
    root = tk.Tk()
    root.geometry('700x550')
    root.title('Smart Thermometer') 

    btn_strt = tk.Button(root, text='Start', command=lambda: detection())
    btn_strt.pack()
    root.mainloop()

if __name__=='__main__':
    start()