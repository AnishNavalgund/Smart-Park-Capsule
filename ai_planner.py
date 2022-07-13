import os
import time
from tkinter import DISABLED
from gui_rev import led_pg, led_spot1, led_spot2, led_spot3, cv, entry2, exit2

# Function to extract the action from the recieved plan
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

    flag = 0
    flag_high = 0

    try:
        if excel_data['humidity'] is not None:
            if excel_data['humidity'] > 55.0:#temp is high
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

    #print("dataaa:"+ excel_data['Lightsensor'])

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