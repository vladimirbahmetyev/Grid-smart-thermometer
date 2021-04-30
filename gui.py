import tkinter as tk
# from tkinter.messagebox import showinfo
# from ttk import Combobox
# from PIL import ImageTk, Image
# from tkinter import filedialog
from go import *

global COLORS, is_end
is_end = False
COLORS = {'y': ['#FFFF99','#FFFF00'],
          'o': ['#FFCC99','#FF8000'],
          'g': ['#CCFFCC','#00FF00'],
          'r': ['#FF9999','#FF0000'],
          'b': ['#9999FF','#0000FF']}

def thermometer(ArduinoSerial):
    for widget in root.winfo_children():
        widget.destroy()

    btn_end = tk.Button(root, text='End', 
                relief="flat",
                font=("Helvetica", 24, "bold"),
                fg="grey",
                bg=COLORS['b'][0],
                activeforeground="grey", 
                activebackground=COLORS['b'][0],
                command=lambda: end())
    btn_end.pack(side=tk.TOP, anchor=tk.NE)
    lbl_th = tk.Label(text='Come Closer')
    lbl_th.place(x=root.winfo_screenwidth()//2,y=root.winfo_screenheight()//2,anchor="center")
    lbl_th.config(font=("Helvetica", 54, "bold"),fg=COLORS['b'][1],bg=COLORS['b'][0])
    # lbl.config(fg=COLORS['b'][1],bg=COLORS['b'][0])
    root.configure(background=COLORS['b'][0])
    root.update()
 
    check = str(ArduinoSerial.readline()) 
    a = str(b'1\r\n')
    b = str(b'2\r\n')
    c = str(b'3\r\n')
    d = str(b'4\r\n')
    while (check != a and not is_end):
        check = str(ArduinoSerial.readline())
        print(check)

        if (check == b):
            lbl_th.destroy()
            lbl_th = tk.Label(text='Move your hand to the sensor')
            lbl_th.config(font=("Helvetica", 54, "bold"),fg=COLORS['b'][1],bg=COLORS['b'][0])
            root.configure(background=COLORS['b'][0])
            btn_end.configure(bg=COLORS['b'][0])
            
        if (check == c):
            lbl_th.destroy()
            lbl_th = tk.Label(text='Temperature is normal,\n come through')
            lbl_th.config(font=("Helvetica", 54, "bold"),fg=COLORS['g'][1],bg=COLORS['g'][0])
            root.configure(background=COLORS['g'][0])
            btn_end.configure(bg=COLORS['g'][0])
            
        if (check == d):
            lbl_th.destroy()
            lbl_th = tk.Label(text='No passage,\n high temperature')
            lbl_th.config(font=("Helvetica", 54, "bold"),fg=COLORS['r'][1],bg=COLORS['r'][0])
            root.configure(background=COLORS['r'][0])
            btn_end.configure(bg=COLORS['g'][0])
        
        lbl_th.place(x=root.winfo_screenwidth()//2,y=root.winfo_screenheight()//2,anchor="center")
        
        root.update()
        # lbl_th.destroy()


def detection():
    # for widget in root.winfo_children():
    #     widget.destroy()

    while not is_end:
        # lbl = tk.Label(text='')
        # lbl.destroy()
        for widget in root.winfo_children():
            widget.destroy() 

        btn_end = tk.Button(root, text='End', 
                    relief="flat",
                    font=("Helvetica", 24, "bold"),
                    fg="grey",
                    bg=root['background'],
                    activeforeground="grey", 
                    activebackground=root['background'],
                    command=lambda: end())
        btn_end.pack(side=tk.TOP, anchor=tk.NE)
        # btn_end.config(fg=COLORS['b'][1], bg=COLORS['b'][0])

        is_person_detected = check_person(camera_stream)
        if is_person_detected == '1':
            ArduinoSerial.write(is_person_detected.encode())  # pass 1
            lbl = tk.Label(text='Human Detected')
            lbl.config(font=("Helvetica", 54, "bold"),fg=COLORS['g'][1],bg=COLORS['g'][0])
            root.configure(background=COLORS['g'][0])
            lbl.place(x=root.winfo_screenwidth()//2,y=root.winfo_screenheight()//2,anchor="center")
            btn_end.configure(bg=COLORS['g'][0])
            root.update()
            time.sleep(2)
            # lbl.destroy()
            thermometer(ArduinoSerial)
            
        else:
            lbl = tk.Label(text='Human Not Detected')
            lbl.config(font=("Helvetica", 54, "bold"),fg=COLORS['r'][1],bg=COLORS['r'][0])
            root.configure(background=COLORS['r'][0])
            lbl.place(x=root.winfo_screenwidth()//2,y=root.winfo_screenheight()//2,anchor="center")
            btn_end.configure(bg=COLORS['r'][0])
            root.update()
            ArduinoSerial.write(is_person_detected.encode())  # pass 0
            time.sleep(2)
            # lbl.destroy()
         
        root.update()

    if is_end:
        # camera_stream.stream.release()
        # cv2.destroyAllWindows()
        start()

def end():
    global is_end
    is_end = True
    # start()

def start():
    global is_end
    is_end = False
    for widget in root.winfo_children():
        widget.destroy()

    root.config(background=COLORS['b'][0])

    btn_strt = tk.Button(root, text='Start', 
                        relief="groove",
                        font=("Helvetica", 54, "bold"),
                        fg=COLORS['b'][1], 
                        bg=COLORS['b'][0],
                        activeforeground=COLORS['b'][1], 
                        activebackground=COLORS['b'][0],
                        highlightcolor="grey",
                        padx=25,pady=25,
                        command=lambda: detection())
    # btn_strt.config(font=("Helvetica", 54, "bold"))
    # btn_strt.config(fg=COLORS['b'][1], bg=COLORS['b'][0])
    
    btn_strt.place(x=root.winfo_screenwidth()//2,y=root.winfo_screenheight()//2,anchor="center")
    

if __name__=='__main__':
    global root, ArduinoSerial, camera_stream
    root = tk.Tk()
    root.overrideredirect(False)
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.title('Smart Thermometer')

    ArduinoSerial = serial.Serial('com3', 9600)  # create an object to work with a serial communication port
    time.sleep(2)  # wait 2 seconds for serial communication to be established
    camera_stream = VideoStream(src=0).start()

    start()
    root.mainloop()