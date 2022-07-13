import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import ast
from tkinter import DISABLED
from gui_rev import disp_temp, cv, root
from ai_planner import run_planner, generate_problemfile

#-------------Initializations---------------#
HostAddress = "192.168.0.222"
SensorTopicName = "temperatureTopic"
PlanTopicName = "temperatureAction"

#--------------Function Definitions------------------#
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