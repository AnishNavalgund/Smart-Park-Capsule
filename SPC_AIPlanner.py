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

File Description: SPC_AIPlanner.py is the main file to perform AI-Planning. The code will generate
                  the plan dynamically as the per the input sensor data.

Timestamp: 10th July 2022

"""
# Import required python packages 
import os
import time
from tkinter import DISABLED
from SPC_GUI import led_pg, led_spot2, cv, entry2, exit2

# Function to extract the action from the recieved plan
def parseFile(filename):

    action_out={}
    f = open(filename, 'r')
    lines = f.readlines()[0:4]

     #to remove first character '('
    for i in range(0,4):
       # lines = lines[1:]
        line_split = lines[i].split()#split at spaces
    
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
    myCmd = 'python SPC_RunOnlineAIPlanner.py {0} {1} {2}'
    myCmd = myCmd.format(domainname, problem, out)
    os.system(myCmd)
    action = parseFile(out)
    return action

def generate_problemfile(excel_data):
    f = open("SPC_ProblemFile.pddl", "w")
    f.write("""(define (problem SPCProblem) (:domain SPCDomain)

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

    flag = 0
    flag_high = 0

    try:
        if excel_data['humidity'] is not None:
            if excel_data['humidity'] > 55.0: #temp is high
                f.write("\t(TempHigh TempSensor)\n")
            elif excel_data['humidity'] <= 55.0:
                f.write("\t(FanOn Fan)\n")
    except:
        print('temp= nan')

    if excel_data['Lightsensor'] <  200 :
        f.write("\n")
        print("In Light IF")
    else:        
        f.write("\t(LuminosityHigh LightSensor)\n\t(LightOn Light)\n") #turn led off
        print("In Light ELSE")

    if excel_data['IR_sensor'] == 1.0 :
        f.write("\t(Notmax Parkingvacancy)\n") #open door
        led_pg.to_green()
    else: 
        f.write("\t(IRHigh IRSensor)\n\t(DoorOpen Door)\n")
        led_pg.to_red()

    if excel_data['Ultrasonic-2'] <= 11.0 :
        f.write("\t(LedOn Led)\n") #off#car present
        led_spot2.to_red()
        flag_high = 1
    else:
        f.write("\t(UltrasonicHigh UltrasonicSensor)\n")
        led_spot2.to_green()

        if((flag == 1)):
            timenow_2out =  time.strftime("%H:%M:%S") 
            exit2.insert(0,timenow_2out)
            exit2.config(state=DISABLED)
            cv.create_window(150, 380, window=exit2)
            flag = 0

    if((flag_high == 1)):
        timenow_2 =  time.strftime("%H:%M:%S") 
        entry2.insert(0,timenow_2)
        entry2.config(state=DISABLED)
        cv.create_window(150, 380, window=entry2)
        flag_high = 0

    f.write(""")

(:goal  (and (TempSuitable TempSensor) (LuminositySuitable LightSensor) (DoorSuitable Door) (suitable UltrasonicSensor));Turn on LED to indicate free spot
)
)""")   
    f.close()