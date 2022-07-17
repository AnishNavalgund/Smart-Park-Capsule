"""
Project:    Smart Park Capsule

Course:     Smart City and IOT
Institute:  Service Computing Department, IAAS, University of Stuttgart

---------------- Team Members -----------

Sl.No   |           Names                   
  1     |     Swathi Shridhar               
  2     |     Badruddin Mukadam             
  3     |     Suraj Sakpal                  
  4     |     Anish Krishna Navalgund       
-----------------------------------------

File Description: SPC_GUI.py creates the real-time visualization window to monitor the 
                  required data in the project. 

Timestamp: 10th July 2022

"""
# Import required python packages 
from   tkinter import *
import tkinter as tk
import tk_tools
from   tkinter.font import BOLD
import time
import datetime as dt
import paho.mqtt.client as paho
import paho.mqtt.publish as publish

# Initializations
root = tk.Tk() # Create a basic root for GUI
cv = Canvas( root, width = 1500, height = 850) # Create a CANVAS environment

root.title('Smart Parking System') # Give the title to the GUI

# Adjust size
root.geometry("1500x850")
root.resizable(True, True)

# Add image file
bg = PhotoImage(file = "SPC_BgImage.png")

# Create Canvas
cv.pack(fill = "both", expand = True)

# Display imagen
cv.create_image( 0, 0, image = bg, anchor = "nw") 

# Add Main Heading to GUI 
cv.create_text( 770, 50, fill="Gold",font="Courier 35 italic bold", text = "Smart Park Capsule")

# Add Parking Spots Heading to GUI
cv.create_text( 200, 150, fill="Cyan",font="Andy 20 bold", text = "Parking Spot - 1")
cv.create_text( 800, 150, fill="Cyan",font="Andy 20 bold", text = "Parking Spot - 2")
cv.create_text( 1300, 150, fill="Cyan",font="Andy 20 bold", text = "Parking Spot - 3")

# Add widgets to record In-Time of vehicles for Parking Spot 1
cv.create_text( 150, 360, fill="Cyan",font="Andy 13 bold", text = "In-Time")
entry1 = tk.Entry (root, justify = CENTER, font=("Times", 10, BOLD))
timenow_1 = time.strftime("%H:%M:%S") 
entry1.insert(0,timenow_1)
entry1.config(state=DISABLED)
cv.create_window(150, 380, window=entry1)

# Add widgets to record Out-Time of vehicles for Parking Spot 1
cv.create_text( 300, 360, fill="Cyan",font="Andy 13 bold", text = "Out-Time")
exit1 = tk.Entry (root, justify = CENTER,font=("Times", 10, BOLD))
exit1.config(state=DISABLED)
cv.create_window(300, 380, window=exit1)

# Add widgets to record In-Time of vehicles for Parking Spot 2
cv.create_text( 730, 360, fill="Cyan",font="Andy 13 bold", text = "In-Time")
entry2 = tk.Entry (root, justify = CENTER, font=("Times", 10, BOLD))
"""timenow_2out =  time.strftime("%H:%M:%S") 
entry2.insert(0,timenow_2out)
entry2.config(state=DISABLED)
cv.create_window(730, 380, window=entry2)"""

# Add widgets to record Out-Time of vehicles for Parking Spot 2
cv.create_text( 880, 360, fill="Cyan",font="Andy 13 bold", text = "Out-Time")
exit2 = tk.Entry (root, justify = CENTER, font=("Times", 10, BOLD))
exit2.config(state=DISABLED)
cv.create_window(880, 380, window=exit2)

# Add widgets to record In-Time of vehicles for Parking Spot 3
cv.create_text( 1250, 360, fill="Cyan",font="Andy 13 bold", text = "In-Time")
entry3 = tk.Entry (root, justify = CENTER, font=("Times", 10, BOLD))
timenow_3 = time_format = time.strftime("%H:%M:%S")
entry3.insert(0,timenow_3)
entry3.config(state=DISABLED)
cv.create_window(1250, 380, window=entry3)

# Add widgets to record Out-Time of vehicles for Parking Spot 3
cv.create_text( 1400, 360, fill="Cyan",font="Andy 13 bold", text = "Out-Time")
exit3 = tk.Entry (root, justify = CENTER,font=("Times", 10, BOLD))
exit3.config(state=DISABLED)
cv.create_window(1400, 380, window=exit3)

# Add occupancy indication for Parking Spot 1
led_spot1 = tk_tools.Led(cv, size=100)
led_canvas = cv.create_window(160,200,anchor="nw",window = led_spot1)
led_spot1.to_red()

# Add occupancy indication for Parking Spot 2
led_spot2 = tk_tools.Led(cv, size=100)
led_canvas = cv.create_window(750,200,anchor="nw",window = led_spot2)
led_spot2.to_grey()

# Add occupancy indication for Parking Spot 3
led_spot3 = tk_tools.Led(cv, size=100)
led_canvas = cv.create_window(1250,200,anchor="nw",window = led_spot3)
led_spot3.to_red()

# Add Parking Gate Heading to GUI
cv.create_text( 400, 450, fill="Yellow",font="Andy 20 bold", text = "Parking Gate")

# Add Parking gate status indication
led_pg = tk_tools.Led(cv, size=100)
led_canvas = cv.create_window(350,500,anchor="nw",window = led_pg)
led_pg.to_grey()

# Add widget to display temperature values
cv.create_text( 1100, 450, fill="Yellow",font="Andy 20 bold", text = "Temperature Values")
disp_temp = tk.Entry (root, justify = CENTER)

# Add widget to display time
time_label = Label(cv, font=("Courier", 12, 'bold'), bg="Black", fg="White", bd =10)
DigitalClock_Label = cv.create_window( 1300, 15, anchor = "nw", window = time_label)

# Function to set-up Digital Clock
def GetCurrentTime():
   time_format = time.strftime("Time:%H:%M:%S")
   time_label.config(text=time_format)
   time_label.after(200, GetCurrentTime)

# Display current time
GetCurrentTime()

# Display current date
date = dt.datetime.now()
date_format = f"{date: %d %b %Y}"
cv.create_text( 1370, 65, fill="White",font="Times 12 bold", text = date_format)
