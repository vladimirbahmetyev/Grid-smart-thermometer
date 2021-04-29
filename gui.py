import tkinter as tk
# from tkinter.messagebox import showinfo
# from ttk import Combobox
# from PIL import ImageTk, Image
# from tkinter import filedialog
from go import *

global COLORS
COLORS = {'y': ['#FFFF99','#FFFF00'],
          'o': ['#FFCC99','#FF8000'],
          'g': ['#CCFFCC','#00FF00'],
          'r': ['#FF9999','#FF0000'],
          'b': ['#9999FF','#0000FF']}

def thermometer(ArduinoSerial):
    lbl_th = tk.Label(text='Come Closer')
    lbl_th.place(x=400,y=250,anchor="center")
    lbl_th.config(font=("Helvetica", 34, "bold"),fg=COLORS['b'][1],bg=COLORS['b'][0])
    # lbl.config(fg=COLORS['b'][1],bg=COLORS['b'][0])
    root.configure(background=COLORS['b'][0])
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
            lbl_th.config(font=("Helvetica", 34, "bold"),fg=COLORS['b'][1],bg=COLORS['b'][0])
            root.configure(background=COLORS['b'][0])
            # lbl_th.place(x=25,y=75)
        if (check == c):
            lbl_th.destroy()
            lbl_th = tk.Label(text='Temperature is normal, come through')
            lbl_th.config(font=("Helvetica", 34, "bold"),fg=COLORS['g'][1],bg=COLORS['g'][0])
            root.configure(background=COLORS['g'][0])
            # lbl_th.place(x=25,y=75)
        if (check == d):
            lbl_th.destroy()
            lbl_th = tk.Label(text='No passage, high temperature')
            lbl_th.config(font=("Helvetica", 34, "bold"),fg=COLORS['r'][1],bg=COLORS['r'][0])
            root.configure(background=COLORS['r'][0])
        
        lbl_th.place(x=400,y=250,anchor="center")
        
        root.update()

def detection():
    for widget in root.winfo_children():
        widget.destroy()
    ArduinoSerial = serial.Serial('com3', 9600)  # create an object to work with a serial communication port
    time.sleep(2)  # wait 2 seconds for serial communication to be established
    camera_stream = VideoStream(src=0).start()
    while True:
        # lbl = tk.Label(text='')
        # lbl.destroy()
        is_person_detected = check_person(camera_stream)
        if is_person_detected == '1':
            ArduinoSerial.write(is_person_detected.encode())  # pass 1
            lbl = tk.Label(text='Human Detected')
            lbl.config(font=("Helvetica", 34, "bold"),fg=COLORS['g'][1],bg=COLORS['g'][0])
            root.configure(background=COLORS['g'][0])
            lbl.place(x=400,y=250,anchor="center")
            root.update()
            time.sleep(3)
            lbl.destroy()
            thermometer(ArduinoSerial)
            
        else:
            lbl = tk.Label(text='Human Not Detected')
            lbl.config(font=("Helvetica", 34, "bold"),fg=COLORS['r'][1],bg=COLORS['r'][0])
            root.configure(background=COLORS['r'][0])
            lbl.place(x=400,y=250,anchor="center")
            root.update()
            ArduinoSerial.write(is_person_detected.encode())  # pass 0
            time.sleep(3)
            lbl.destroy()
         
        root.update()

def start_pressed():
    detection()

def start():
    global root
    root = tk.Tk()
    root.geometry('800x500')
    root.title('Smart Thermometer') 

    btn_strt = tk.Button(root, text='Start', command=lambda: start_pressed())
    btn_strt.config(font=("Helvetica", 34, "bold"))
    btn_strt.config(fg=COLORS['b'][1], bg=COLORS['b'][0])
    root.config(background=COLORS['b'][0])
    btn_strt.place(x=400,y=250,anchor="center")
    root.mainloop()

if __name__=='__main__':
    start()