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

#-------------Initializations---------------#
HostAddress = "192.168.0.222"
SensorTopicName = "temperatureTopic"
PlanTopicName = "temperatureAction"

"""file = open("data.csv", "w")
writer = csv.writer(file)
writer.writerow(["Time", "Temperature", "Humidity", "Light", "Motion", "Ultrasonic"])
"""

#--------------Function Definitions------------------#
#Function to extract the action from the recieved plan
def parseFile(filename):
    action={}
    f = open(filename, 'r')
    lines = f.readlines()[0:4]
     #to remove first character '('
    for i in range(0,4):
       # lines = lines[1:]
        line_split = lines[i].split()#split at spaces
        action[i]=line_split[0]
        #print(action[i])
    
    return action

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
    if excel_data['temperature'] is not None:
        if excel_data['temperature'] > 22:
            f.write("\t(TempHigh TempSensor)\n")
        elif excel_data['temperature'] <= 22:
            f.write("\t(FanOn Fan)\n")

    if excel_data['Lightsensor'] >= 300.0 :
        f.write("\t(LuminosityHigh LightSensor)\n\t(LightOn Light)\n") #turn led off
    else:
        f.write("\n")
    
    if excel_data['Motion_sensor'] == 1.0 :
        f.write("\t(Notmax Parkingvacancy)\n") #open door
    else: 
        f.write("\t(IRHigh IRSensor)\n\t(DoorOpen Door)\n")

    if excel_data['Ultrasonic-2'] <= 200.0 :
        f.write("\t(LedOn Led)\n") #off
    else:
        f.write("\t(UltrasonicHigh UltrasonicSensor)\n")
        
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
    excel_data = {'timeStamp': None, 'temperature': None, 'humidity': None, 'Lightsensor':None, 'Motion_sensor': None, 'Ultrasonic-2': None}
    if 'timeStamp' in payload_data and payload_data['timeStamp'] is not None:
        excel_data['timeStamp'] = payload_data['timeStamp']
    if 'temperature' in payload_data and payload_data['temperature'] is not None:
        excel_data['temperature'] = payload_data['temperature']
    if 'humidity' in payload_data and payload_data['humidity'] is not None:
        excel_data['humidity'] = payload_data['humidity']
    if 'Lightsensor' in payload_data and payload_data['Lightsensor'] is not None:
        excel_data['Lightsensor'] = payload_data['Lightsensor']
    if 'Motion_sensor' in payload_data and payload_data['Motion_sensor'] is not None:
        excel_data['Motion_sensor'] = payload_data['Motion_sensor']
    if 'Ultrasonic-2' in payload_data and payload_data['Ultrasonic-2'] is not None:
        excel_data['Ultrasonic-2'] = payload_data['Ultrasonic-2']
    
    #print("msg sent: temperature " + "%.1f" % temperature +"  humidity " + "%.1f" % humidity +" Ultrasonic-1 " + "%.1f" % us +" Ultrasonic-2 " + "%.1f" % us2 +" Lightsensor :" + "%.1f" % light  +" Motion_sensor:  " + "%.1f" % motion +" IR_sensor:  " + "%.1f" % ir   ) # Print sent temperature msg on console
   
    print(f"Excel data : {excel_data}")
   # writer.writerow([excel_data['timeStamp'], excel_data['temperature'], excel_data['humidity'], excel_data['Lightsensor'],excel_data['Motion_sensor'], excel_data['Ultrasonic-2']])
    
    """TempAction = None
    LightAction = None
    GateAction = None
    UltrasonicAction = None"""
    #---------select problem files according to the sensor data-------#
    domainname= 'Domainnew.pddl' #select domain file
    filename = 'temp.text'
    #----Generate Problem file------#
    generate_problemfile(excel_data)
    problem = 'testproblemfile.pddl'
    problem = 'testproblemfile.pddl'
    Action = run_planner(domainname, problem, filename)
    print(f"action : {Action}")  

    action_out={}
    action_out['temp_action'] = Action[1]
    action_out['light_action'] = Action[0]
    action_out['pir_action'] = Action[3]
    action_out['ultra_action'] = Action[2]
    print(action_out)
    mqtt_payload = str(action_out)
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

while 1:
    client.loop_forever()  # contineously checking for message