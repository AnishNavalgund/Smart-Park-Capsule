#pc
import csv
import os
import re
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import time
import sys
import datetime
import time
import json
import ast

#broker = "localhost"  # host name
#topic = "indoor"  # topic name
MQTT_SERVER = "192.168.0.222"
MQTT_PATH = "temperatureTopic"
PDDL_TOPIC = "temperatureAction"

def parseFile(filename):
    f = open(filename, 'r+')
    lines = f.readlines()[0]
    f.close()

    lines = lines[1:]
    line_split = lines.split()
    action1 = line_split[0]
    print(action1)
    return action1


def run_planner(domainname, problem, out):
    myCmd = 'python Aiplanner.py {0} {1} {2}'
    myCmd = myCmd.format(domainname, problem, out)
    os.system(myCmd)
    action = parseFile(out)
    return action

def on_message(client, userdata, message):
    global writer
    s = str(message.payload.decode("utf-8"))
    print("Received msg is ", s)
    # payload_data = json.loads(s)
    payload_data = ast.literal_eval(s)
    excel_data = {'timeStamp': None, 'temperature': None, 'humidity': None}
    if 'timeStamp' in payload_data and payload_data['timeStamp'] is not None:
        excel_data['timeStamp'] = payload_data['timeStamp']
    if 'temperature' in payload_data and payload_data['temperature'] is not None:
        excel_data['temperature'] = payload_data['temperature']
    if 'humidity' in payload_data and payload_data['humidity'] is not None:
        excel_data['humidity'] = payload_data['humidity']
    
    
    print(f"Excel data : {excel_data}")
    temp_action = None
    domainname= 'Domain.pddl'
    filename = 'temp.text'
    if excel_data['temperature'] is not None:
        if excel_data['temperature'] > 22:
            problem = 'Temp_ProblemHIGH.pddl'
            temp_action = run_planner(domainname, problem, filename)
        elif excel_data['temperature'] <= 22:
            problem = 'Temp_ProblemLOW.pddl'
            temp_action = run_planner(domainname, problem, filename)
    print(f"temp_action : {temp_action}")

    action = {}
    
    action['temp_action'] = temp_action
    mqtt_payload = str(action)
    print(mqtt_payload)
    publish.single(PDDL_TOPIC, mqtt_payload, hostname="192.168.0.222")
    

def on_connect(client, userdata, flags, rc):
    client.subscribe(MQTT_PATH)

client = paho.Client()  # create client object

client.on_connect = on_connect
client.on_message = on_message
print("connecting to broker host")
client.connect(MQTT_SERVER,1883,60)  # connection establishment with broker
print("subscribing begins here")
client.subscribe(MQTT_PATH)  # subscribe topic test

while 1:
    client.loop_forever()  # contineously checking for message