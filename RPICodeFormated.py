import threading
import paho.mqtt.client as paho
import ssl
import grovepi
import RPi.GPIO as GPIO
import time
from time import sleep
import datetime
from random import uniform
import paho.mqtt.publish as publish
import ast

#--------------Initializations--------------# 

HostAddress="192.168.0.222"
PlanTopic = "temperatureAction"

#temperature & humidity sensor 
TempPort = 7 
TempSensor = 0 
TempTimeout = 1

#light sensor
LightSensor = 0

#PIR motion sensor
PIRSensor = 8
Motion=0

#ultra-sonic sensor
Ultrasonic_ranger = 5
Ultrasonic_ranger2 = 6

#motor and IR
mode = GPIO.getmode()
IRSensor = 18
Forward=24
Backward=23
SleepTime=1
GPIO.setmode(GPIO.BCM)
GPIO.setup(IRSensor,GPIO.IN)

# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")
GPIO.setup(Forward, GPIO.OUT)
GPIO.setup(Backward, GPIO.OUT)


def forward(x):
 GPIO.output(Forward, GPIO.HIGH)
 print("Moving Forward")
 time.sleep(x)
 GPIO.output(Forward, GPIO.LOW)
#---------------Function Definitions----------#
def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print("Connected to AWS")
    connflag = True
    print("Connection returned result: " + str(rc) )
######on_message defined twice??????????????/
def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))

def pddlMQTTDataReceive():
    print("MQTT PDDL Data receive thread started....... :)")
    pddl_mqtt_client.subscribe(PlanTopic)  # subscribe topic test
    pddl_mqtt_client.loop_forever()

def on_message(client, userdata, message):
    global writer
    action = str(message.payload.decode("utf-8"))
    print("Received msg is ", action)
    # payload_data = json.loads(s)
    payload_pddl = ast.literal_eval(action)
    
    temp_output = None    

    if 'temp_action' in payload_pddl and payload_pddl['temp_action'] is not None:
        temp_output = payload_pddl['temp_action']
    
    cooler_actuation(temp_output)


def cooler_actuation(temp_output):
    if temp_output is not None:
        forward(5)
        print("Hello")   




mqttc = paho.Client()
client= paho.Client()

client.connect("192.168.0.222",1883,60)

mqttc.on_connect = on_connect
mqttc.on_message = on_message    

#subscribe from pddl
pddl_mqtt_client = paho.Client("PDDL")  # create client object
pddl_mqtt_client.on_message = on_message
print("connecting to broker host", HostAddress)
pddl_mqtt_client.connect(HostAddress)  # connection establishment with broker

def pddlMQTTDataReceive():
    print("MQTT PDDL Data receive thread started....... :)")
    pddl_mqtt_client.subscribe(PlanTopic)  # subscribe topic test
    pddl_mqtt_client.loop_forever()

def sensordatapublish():
    sleep(5)
    if connflag == True:
        timeStamp = datetime.datetime.now()
        tempreading = uniform(20.0,25.0)
        
        # Generating Temperature Readings
        [temperature, humidity] = grovepi.dht(TempPort, TempSensor)
        # Generating Ultrasonic Readings
        us= grovepi.ultrasonicRead(Ultrasonic_ranger)
        us2= grovepi.ultrasonicRead(Ultrasonic_ranger2)
        # Generating Lightsensor Readings
        light= grovepi.analogRead(LightSensor)
        # Calculate resistance of sensor in K
        resistance = (float)(1023 - light) * 10 / light
        
        if GPIO.input(IRSensor):
            ir = 1
        else:
            ir = 0 
        
        motion=grovepi.digitalRead(PIRSensor)
        #if motion==0 or motion==1:  # check if reads were 0 or 1 it can be 255 also because of IO Errors so remove those values
           # if motion==1:
           #     print ('Motion Detected')
           # else:
           #     print ('-')
            # if your hold time is less than this, you might not see as many detections
        #time.sleep(.1)
        message = '{"timeStamp":'+'"'+str(timeStamp)+'",'+'"temperature":'+str(temperature)+','+'"humidity":'+str(humidity) +','+'"Ultrasonic-1":'+str(us)+','+'"Ultrasonic-2":'+str(us2)+','+'"Lightsensor":'+str(light) +','+'"Light_resistance":'+str(resistance) +','+'"PIR_motion_sensor":'+str(motion) +','+'"IR_sensor":'+str(ir) + '}'
        mqttc.publish("temperatureTopic", message, 1)        # topic: temperature # Publishing Temperature values
        client.publish("temperatureTopic", message, 1)  
        print("msg sent: temperature " + "%.1f" % temperature +"  humidity " + "%.1f" % humidity +" Ultrasonic-1 " + "%.1f" % us +" Ultrasonic-2 " + "%.1f" % us2 +" Lightsensor :" + "%.1f" % light  +" Motion_sensor:  " + "%.1f" % motion +" IR_sensor:  " + "%.1f" % ir   ) # Print sent temperature msg on console
    else:
        print("waiting for connection...")    
        

awshost = "a2ngemuw19bbnm-ats.iot.eu-central-1.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.   
clientId = "myLaptop"                                     # Thing_Name
thingName = "Raspberrypi"                                    # Thing_Name
caPath = "/home/pi/Public/AWS_IOT/AmazonRootCA1.pem" #Amazon's certificate from Third party                                     # Root_CA_Certificate_Name
certPath = "/home/pi/Public/AWS_IOT/certificate.pem.crt"   # <Thing_Name>.cert.pem.crt. Thing's certificate from Amazon
keyPath = "/home/pi/Public/AWS_IOT/private.pem.key"        # <Thing_Name>.private.key Thing's private key from Amazon
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
mqttc.loop_start()                                          # Start the loop

#---------Start threads to publish sensor data and recieve the plan ---------#
t1 = threading.Thread(target=sensordatapublish)
t2 = threading.Thread(target=pddlMQTTDataReceive)
t1.start()
t2.start()