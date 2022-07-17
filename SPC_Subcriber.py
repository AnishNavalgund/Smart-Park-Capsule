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

File Description: SPC_Subcriber.py is the main code to run in the project. This code connects 
                  to the Raspberry Pi through MQTT protocol and subscibes to the sensor data. 
                  This code also runs the AI-planner as and when the sensor data is subscribed. 

Timestamp: 10th July 2022

"""

# Import required python packages 
import csv
import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import ast
from   tkinter import DISABLED
from   SPC_GUI import disp_temp, cv, root
from   SPC_AIPlanner import run_planner, generate_problemfile

# Initializations
HostAddress     = "192.168.0.222"          #Connect to RaspberryPi IP
SensorTopicName = "temperatureTopic"   #Subscribe to topic
PlanTopicName   = "temperatureAction"

#
#file = open("iotdata.csv", "w")
with open("iotdata.csv", 'w') as file: 
    writer = csv.writer(file)
    writer.writerow(["Time", "Temperature", "Humidity", "Luminosity", "Gate", "Occupancy"])

# Extract the sensor data 
def on_message(client, userdata, message):

    global writer
    get_msg = str(message.payload.decode("utf-8")) # Get the message in form of a string
    print("Received Message:  ", get_msg)          # Print the message string

    message_data = ast.literal_eval(get_msg)

    # Extract sensors data as Dictionary 
    extract_sensor_data = {'timeStamp': None, 'temperature': None, 'humidity': None, 'Lightsensor':None, 'IR_sensor': None, 'Ultrasonic-2': None}
    
    # Extract TimeStamp 
    if 'timeStamp' in message_data and message_data['timeStamp'] is not None:
        extract_sensor_data['timeStamp'] = message_data['timeStamp']

    # Extract Temperature Sensor values 
    if 'temperature' in message_data and message_data['temperature'] is not None:
        extract_sensor_data['temperature'] = message_data['temperature']
        
        # Display the temperature readings on the GUI
        tempData = extract_sensor_data['temperature']
        disp_temp.insert(0,tempData)
        disp_temp.config(state=DISABLED)
        cv.create_window(1100, 510, window=disp_temp)

    # Extract Humidity Sensor values 
    if 'humidity' in message_data and message_data['humidity'] is not None:
        extract_sensor_data['humidity'] = message_data['humidity']

    # Extract Lightsensor Sensor values 
    if 'Lightsensor' in message_data and message_data['Lightsensor'] is not None:
        extract_sensor_data['Lightsensor'] = message_data['Lightsensor']

    # Extract IR-sensor Sensor values 
    if 'IR_sensor' in message_data and message_data['IR_sensor'] is not None:
        extract_sensor_data['IR_sensor'] = message_data['IR_sensor']

    # Extract Ultrasonic Sensor values 
    if 'Ultrasonic-2' in message_data and message_data['Ultrasonic-2'] is not None:
        extract_sensor_data['Ultrasonic-2'] = message_data['Ultrasonic-2']
   
    print(f"Subcribed Sensor Data : {extract_sensor_data}")
    #with open("iotdata.csv", 'w') as csvfile:
    with open("iotdata.csv", 'a') as file:  
        writer = csv.writer(file)
        writer.writerow([extract_sensor_data['timeStamp'], extract_sensor_data['temperature'], extract_sensor_data['humidity'], extract_sensor_data['Lightsensor'],
                     extract_sensor_data['IR_sensor'], extract_sensor_data['Ultrasonic-2']])

# Variables for actuation 

    # AI Planning Actions
    domainname= 'SPC_DomainFile.pddl'   # Select domain file
    filename = 'SPC_GeneratedPlan.text' # Select the text file to which plan has to be written

    generate_problemfile(extract_sensor_data) # Generate Problem file
    problem = 'SPC_ProblemFile.pddl'
    
    Action = run_planner(domainname, problem, filename) #Run AI Planner
    print(f"action : {Action}")  
    mqtt_msg = str(Action) 
    print(f"sent message : {mqtt_msg}")
    publish.single(PlanTopicName, mqtt_msg, hostname="192.168.0.222")

#Subscibe to client when on_connect() is called    
def on_connect(client, userdata, flags, rc):
    client.subscribe(SensorTopicName)

client = paho.Client()  # create client object

client.on_connect = on_connect   # Begin the connection
client.on_message = on_message   # Get messages from client

print("Connecting to broker host")
client.connect(HostAddress,1883,60)  # Establish connect with the broker

print("Subscribing To The Sensor Data Now")
client.subscribe(SensorTopicName)  # subscribe to broker topic 

client.loop_start()  # Start the loop for getting messages
root.mainloop()      # Run GUI for visualization
