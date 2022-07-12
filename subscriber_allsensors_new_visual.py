#pc
import csv
import os
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import time
import sys
import datetime
import json
import ast

from tkinter import *
import tkinter as tk
import tk_tools
import time
import datetime as dt

#-------------Initializations---------------#
HostAddress = "192.168.0.222"
SensorTopicName = "temperatureTopic"
PlanTopicName = "temperatureAction"


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

#--------------Function Definitions------------------#
#Function to extract the action from the recieved plan
def parseFile(filename):
    action_out={}
    f = open(filename, 'r')
    lines = f.readlines()[0:4]
     #to remove first character '('
    for i in range(0,4):
       # lines = lines[1:]
        line_split = lines[i].split()#split at spaces
        
        #print(action[i])
    
        if '(decreasetemperature' in line_split[0] or '(increasetemperature' in line_split[0]:
            action_out['temp_action'] = line_split[0]
        elif '(opendoor' in line_split[0] or '(closedoor' in line_split[0]:
            action_out['pir_action'] = line_split[0]
        elif '(switchonlight' in line_split[0] or '(switchofflight' in line_split[0]:
            action_out['light_action'] = line_split[0]
        elif '(spotnotoccupied' in line_split[0] or '(spotoccupied' in line_split[0]:
            action_out['ultra_action'] = line_split[0]
        else:
            print('error')
    return action_out

#Function to call the planner via command line statement by passing the planner.py Domain.pddl Problem.pddl plan.text
def run_planner(domainname, problem, out):
    myCmd = 'python Aiplanner.py {0} {1} {2}'
    myCmd = myCmd.format(domainname, problem, out)
    os.system(myCmd)
    action = parseFile(out)
    return action

def generate_problemfile(excel_data):
    f = open("testproblemfile.pddl", "w")
    f.write("""(define (problem ABSProblemnew) (:domain ABSSDomainnew)

(:objects 
    TempSensor - sensor
    Fan - actuator

    LightSensor - sensor
    Light - actuator

    IRSensor - sensor
    Door - actuator
    Parkingvacancy - spot
        
    UltrasonicSensor - sensor
    Led - actuator
    

)

(:init""")
    f.write("\n")
    try:
        if excel_data['humidity'] is not None:
            if excel_data['humidity'] > 55.0:#temp is high
                f.write("\t(TempHigh TempSensor)\n")
            elif excel_data['humidity'] <= 55.0:
                f.write("\t(FanOn Fan)\n")
    except:
        print('temp= nan')

    if excel_data['Lightsensor'] >= 300.0 :
        f.write("\t(LuminosityHigh LightSensor)\n\t(LightOn Light)\n") #turn led off
    else:
        f.write("\n")
    
    if excel_data['IR_sensor'] == 1.0 :
        f.write("\t(Notmax Parkingvacancy)\n") #open door
        led_pg.to_green()
    else: 
        f.write("\t(IRHigh IRSensor)\n\t(DoorOpen Door)\n")
        led_pg.to_red()

    if excel_data['Ultrasonic-2'] <= 11.0 :
        f.write("\t(LedOn Led)\n") #off#car present
        led_spot2.to_red()
        #time_now = 
        #disp_temp.insert(0,tempData)
        #disp_temp.config(state=DISABLED)
        #cv.create_window(1100, 510, window=disp_temp)
    else:
        f.write("\t(UltrasonicHigh UltrasonicSensor)\n")
        led_spot2.to_green()
        
    f.write(""")

(:goal  (and (TempSuitable TempSensor) (LuminositySuitable LightSensor) (DoorSuitable Door) (suitable UltrasonicSensor));Turn on LED to indicate free spot
)
)""")   
    f.close()

def on_message(client, userdata, message):
    global writer
    s = str(message.payload.decode("utf-8"))
    print("Received msg is ", s)
    payload_data = ast.literal_eval(s)
    excel_data = {'timeStamp': None, 'temperature': None, 'humidity': None, 'Lightsensor':None, 'IR_sensor': None, 'Ultrasonic-2': None}
    if 'timeStamp' in payload_data and payload_data['timeStamp'] is not None:
        excel_data['timeStamp'] = payload_data['timeStamp']
    if 'temperature' in payload_data and payload_data['temperature'] is not None:
        excel_data['temperature'] = payload_data['temperature']
        tempData = excel_data['temperature']
        disp_temp.insert(0,tempData)
        disp_temp.config(state=DISABLED)
        cv.create_window(1100, 510, window=disp_temp)

    if 'humidity' in payload_data and payload_data['humidity'] is not None:
        excel_data['humidity'] = payload_data['humidity']
    if 'Lightsensor' in payload_data and payload_data['Lightsensor'] is not None:
        excel_data['Lightsensor'] = payload_data['Lightsensor']
    if 'IR_sensor' in payload_data and payload_data['IR_sensor'] is not None:
        excel_data['IR_sensor'] = payload_data['IR_sensor']
    if 'Ultrasonic-2' in payload_data and payload_data['Ultrasonic-2'] is not None:
        excel_data['Ultrasonic-2'] = payload_data['Ultrasonic-2']
    
    #print("msg sent: temperature " + "%.1f" % temperature +"  humidity " + "%.1f" % humidity +" Ultrasonic-1 " + "%.1f" % us +" Ultrasonic-2 " + "%.1f" % us2 +" Lightsensor :" + "%.1f" % light  +" Motion_sensor:  " + "%.1f" % motion +" IR_sensor:  " + "%.1f" % ir   ) # Print sent temperature msg on console
   
    print(f"Excel data : {excel_data}")
   
    
    #---------select problem files according to the sensor data-------#
    domainname= 'Domainnew.pddl' #select domain file
    filename = 'temp.text'
    #----Generate Problem file------#
    generate_problemfile(excel_data)
    problem = 'testproblemfile.pddl'
    
    Action = run_planner(domainname, problem, filename)
    print(f"action : {Action}")  
    #print(Action)
    mqtt_payload = str(Action)
    print(mqtt_payload)
    publish.single(PlanTopicName, mqtt_payload, hostname="192.168.0.222")
    

def on_connect(client, userdata, flags, rc):
    client.subscribe(SensorTopicName)

client = paho.Client()  # create client object

client.on_connect = on_connect
client.on_message = on_message
print("connecting to broker host")
client.connect(HostAddress,1883,60)  # connection establishment with broker
print("subscribing begins here")
client.subscribe(SensorTopicName)  # subscribe topic test

client.loop_start()  # contineously checking for message
root.mainloop() 