from tkinter import *
import tkinter as tk
import tk_tools
import time
import datetime as dt

#-------------Initializations---------------#

root = tk.Tk()
cv = Canvas( root, width = 1500, height = 850)



root.title('Smart Parking System')

# Adjust size
root.geometry("1500x850")
root.resizable(False, False)

   # Add image file
bg = PhotoImage(file = "ParkTest1.png")

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
entry1 = tk.Entry (root, justify = CENTER)
entry1.config(state=DISABLED)
cv.create_window(150, 380, window=entry1)

# Add widgets to record Out-Time of vehicles for Parking Spot 1
cv.create_text( 300, 360, fill="Cyan",font="Andy 13 bold", text = "Out-Time")
exit1 = tk.Entry (root, justify = CENTER)
exit1.config(state=DISABLED)
cv.create_window(300, 380, window=exit1)

# Add widgets to record In-Time of vehicles for Parking Spot 2
cv.create_text( 730, 360, fill="Cyan",font="Andy 13 bold", text = "In-Time")
entry2 = tk.Entry (root, justify = CENTER)
entry2.config(state=DISABLED)
cv.create_window(730, 380, window=entry2)

# Add widgets to record Out-Time of vehicles for Parking Spot 2
cv.create_text( 880, 360, fill="Cyan",font="Andy 13 bold", text = "Out-Time")
exit2 = tk.Entry (root, justify = CENTER)
exit2.config(state=DISABLED)
cv.create_window(880, 380, window=exit2)

# Add widgets to record In-Time of vehicles for Parking Spot 3
cv.create_text( 1250, 360, fill="Cyan",font="Andy 13 bold", text = "In-Time")
entry3 = tk.Entry (root, justify = CENTER)
entry3.config(state=DISABLED)
cv.create_window(1250, 380, window=entry3)

# Add widgets to record Out-Time of vehicles for Parking Spot 3
cv.create_text( 1400, 360, fill="Cyan",font="Andy 13 bold", text = "Out-Time")
exit3 = tk.Entry (root, justify = CENTER)
exit3.config(state=DISABLED)
cv.create_window(1400, 380, window=exit3)

# Add occupancy indication for Parking Spot 1
led_spot1 = tk_tools.Led(cv, size=100)
led_canvas = cv.create_window(160,200,anchor="nw",window = led_spot1)
led_spot1.to_grey()

# Add occupancy indication for Parking Spot 2
led_spot2 = tk_tools.Led(cv, size=100)
led_canvas = cv.create_window(750,200,anchor="nw",window = led_spot2)
led_spot2.to_grey()

# Add occupancy indication for Parking Spot 3
led_spot3 = tk_tools.Led(cv, size=100)
led_canvas = cv.create_window(1250,200,anchor="nw",window = led_spot3)
led_spot3.to_grey()

# Add Parking Gate Heading to GUI
cv.create_text( 400, 450, fill="Yellow",font="Andy 20 bold", text = "Parking Gate")

# Add Parking gate status indication
led_pg = tk_tools.Led(cv, size=100)
led_canvas = cv.create_window(350,500,anchor="nw",window = led_pg)
led_pg.to_grey()

# Add widget to display temperature values
cv.create_text( 1100, 450, fill="Yellow",font="Andy 20 bold", text = "Temperature Values")
disp_temp = tk.Entry (root, justify = CENTER)
disp_temp.config(state=DISABLED)
cv.create_window(1100, 510, window=disp_temp)

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
 


def fortest(i):

    if (i == 2): #Ultra1
            led_spot1.to_red()
            print("In red")
    else:
            print("In green")
            led_spot1.to_green()
   
    i = i+1
    root.after(2000, fortest(i))  # reschedule event in 2 seconds

root.mainloop() 
