from tkinter import *
import tkinter as tk
import tk_tools
import time
import datetime as dt
#import random
import json

root =tk.Tk()
root. title('Smart Parking System')

# Adjust size
root.geometry("1500x850")
root.resizable(False, False)

# Add image file
bg = PhotoImage(file = "ParkTest1.png")

# Create Canvas
canvas1 = Canvas( root, width = 1500, height = 850)

canvas1.pack(fill = "both", expand = True)

# Display image
canvas1.create_image( 0, 0, image = bg, anchor = "nw") 

# Add Text 
canvas1.create_text( 800, 50, fill="Blue",font="Times 30 italic bold", text = "Smart Park Capsule")

canvas1.create_text( 200, 150, fill="Cyan",font="Andy 20 bold", text = "Parking Spot - 1")
canvas1.create_text( 800, 150, fill="Cyan",font="Andy 20 bold", text = "Parking Spot - 2")
canvas1.create_text( 1300, 150, fill="Cyan",font="Andy 20 bold", text = "Parking Spot - 3")

canvas1.create_text( 150, 360, fill="Cyan",font="Andy 13 bold", text = "In_Time")
entry1 = tk.Entry (root) 
canvas1.create_window(150, 380, window=entry1)

canvas1.create_text( 300, 360, fill="Cyan",font="Andy 13 bold", text = "Out_Time")
entry2 = tk.Entry (root) 
canvas1.create_window(300, 380, window=entry2)

canvas1.create_text( 730, 360, fill="Cyan",font="Andy 13 bold", text = "In_Time")
entry3 = tk.Entry (root) 
canvas1.create_window(730, 380, window=entry3)

canvas1.create_text( 880, 360, fill="Cyan",font="Andy 13 bold", text = "Out_Time")
entry4 = tk.Entry (root) 
canvas1.create_window(880, 380, window=entry4)

canvas1.create_text( 1250, 360, fill="Cyan",font="Andy 13 bold", text = "In_Time")
entry5 = tk.Entry (root) 
canvas1.create_window(1250, 380, window=entry5)

canvas1.create_text( 1400, 360, fill="Cyan",font="Andy 13 bold", text = "Out_Time")
entry6 = tk.Entry (root) 
canvas1.create_window(1400, 380, window=entry6)


led = tk_tools.Led(canvas1, size=100)
# led.grid(row=5, column=0, sticky='news')
led_canvas = canvas1.create_window(170,200,anchor="nw",window = led)
#led.pack()
led.to_grey()

led1 = tk_tools.Led(canvas1, size=100)
# led.grid(row=5, column=0, sticky='news')
led_canvas = canvas1.create_window(770,200,anchor="nw",window = led1)
#led.pack()
led1.to_grey()

led2 = tk_tools.Led(canvas1, size=100)
# led.grid(row=5, column=0, sticky='news')
led_canvas = canvas1.create_window(1250,200,anchor="nw",window = led2)
#led.pack()
led2.to_grey()

canvas1.create_text( 400, 500, fill="Yellow",font="Andy 20 bold", text = "Parking Gate")

led3 = tk_tools.Led(canvas1, size=100)
# led.grid(row=5, column=0, sticky='news')
led_canvas = canvas1.create_window(350,550,anchor="nw",window = led3)
#led.pack()
led2.to_grey()

canvas1.create_text( 1100, 500, fill="Yellow",font="Andy 20 bold", text = "Temperature Monitor")

def digitalclock():
   text_input = time.strftime("Time:%H:%M:%S")
   label.config(text=text_input)
   label.after(200, digitalclock)
   
label = Label(canvas1, font=("Courier", 12, 'bold'), bg="Black", fg="White", bd =10)
DigitalCLock_Label = canvas1.create_window( 1300, 15, anchor = "nw", window = label)

date = dt.datetime.now()
format_date = f"{date: %d %b %Y}"
#display(format_date)
canvas1.create_text( 1370, 65, fill="White",font="Times 12 bold", text = format_date)

#topic1 = Label(canvas1, font=("Courier", 30, 'bold'), bg="lightblue", fg="black", bd =80)
#button1_canvas = canvas1.create_window( 50, 150, anchor = "nw",window = topic1)

#topic2 = Label(canvas1, font=("Courier", 30, 'bold'), bg="lightblue", fg="black", bd =80)
#button2_canvas = canvas1.create_window( 620, 150,anchor = "nw",window = topic2)

#TempDisplay()
digitalclock()

# Execute tkinter
root.mainloop()
