import threading
import paho.mqtt.client as paho
import ssl
import grovepi
from grovepi import *
from grove_rgb_lcd import *
import RPi.GPIO as GPIO
import time
from time import sleep
import datetime
from random import uniform
import paho.mqtt.publish as publish
import ast
import math

#--------------Initializations--------------# 

HostAddress="192.168.0.222"
PlanTopic = "temperatureAction"

#temperature & humidity sensor 
TempPort = 7 
TempSensor = 0 
TempTimeout = 1

#light sensor
LightSensor = 0

# Connect the Grove LED to digital port D3
led = 3
pinMode(led,"OUTPUT")

# Connect the Grove LED to digital port D5 for resemblence of Led strip
led_strip = 5
pinMode(led_strip,"OUTPUT")

# Connect the Grove Buzzer to digital port D2
# SIG,NC,VCC,GND
buzzer = 2
grovepi.pinMode(buzzer,"OUTPUT")

#IR  sensor
PIRSensor = 8
IR=0

#ultra-sonic sensor
Ultrasonic_ranger = 5
Ultrasonic_ranger2 = 6

#motor and IR
#mode = GPIO.getmode()
IRSensor = 18
Forward=24
Backward=23
SleepTime=1
#GPIO.setup(IRSensor,GPIO.IN)
notmax=1
count_flag = 0

# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")
GPIO.setmode(GPIO.BCM)
GPIO.setup(Forward, GPIO.OUT)
GPIO.setup(Backward, GPIO.OUT)
#servo motor intidef init():
GPIO.setup(17,GPIO.OUT)
servo = GPIO.PWM(17,50) 
servo.start(0)


def IR():
    #GPIO.setmode(GPIO.BCM)
    GPIO.setup(IRSensor, GPIO.IN)
    if GPIO.input(IRSensor):
            ir = 1
    else:
            ir = 0 
    #GPIO.cleanup()
    return ir
    
def fanoff():
    GPIO.output(Forward, GPIO.HIGH)
    print("FAN Off")
    time.sleep(0.9)
    #GPIO.output(Forward, GPIO.LOW)
    
def fanon():
    print("FAN On")
    #time.sleep(0.2)
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
    light_output = None
    pir_output = None
    ultra_output = None
    #Actuator actions
    if 'temp_action' in payload_pddl and payload_pddl['temp_action'] is not None:
        temp_output = payload_pddl['temp_action']
    if 'light_action' in payload_pddl and payload_pddl['light_action'] is not None:
        light_output = payload_pddl['light_action']
    if 'pir_action' in payload_pddl and payload_pddl['pir_action'] is not None:
        pir_output = payload_pddl['pir_action']
    if 'ultra_action' in payload_pddl and payload_pddl['ultra_action'] is not None:
        ultra_output = payload_pddl['ultra_action']

    cooler_actuation(temp_output)
    light_actuation(light_output)
    gate_actuation(pir_output,ultra_output)
    ultra_actuation(ultra_output)

def cooler_actuation(temp_output):
    print(temp_output)
    if temp_output is not None:
        #add temp actions
        
        if temp_output == '(increasetemperature':
            fanoff()
        else:
            fanon()
            
        

def light_actuation(light_output):
    #LED_PIN = 18#################################
    #GPIO.setup(LED_PIN, GPIO.OUT)
    if light_output is not None:
        if light_output == '(switchonlight':
            print("LIGHTS: ON")
            digitalWrite(led_strip,1)  
            #GPIO.output(LED_PIN, True)
        else:
            print("LIGHTS: OFF")
            digitalWrite(led_strip,0)	
           # GPIO.output(LED_PIN, False)
def gate_actuation(pir_output,ultra_output):
    if pir_output is not None:
        servo.start(0)
        #print(pir_output)
        if pir_output == '(opendoor' and ultra_output == '(spotoccupied':
            setText("Parking spots \n full! SORRY:(")
            setRGB(0,0,64)
            grovepi.digitalWrite(buzzer,1)
            time.sleep(1)
            # Stop buzzing for 1 second 
            grovepi.digitalWrite(buzzer,0)
            time.sleep(0.5)
            grovepi.digitalWrite(buzzer,1)
            time.sleep(1)
            grovepi.digitalWrite(buzzer,0)
            print("Door is close")
            
        elif pir_output == '(opendoor' and ultra_output != '(spotoccupied':
            print ("Opening the door !")
            setText(" Welcome!Free spots available.")
            #print ("Opening the main door !") 
            servo.ChangeDutyCycle(7)
            time.sleep(0.5)
            servo.ChangeDutyCycle(0)
            time.sleep(3)
            #turn back to 0 degrees
            print ("Turning back to 0 degrees")
            servo.ChangeDutyCycle(2)
            time.sleep(0.5)
            servo.ChangeDutyCycle(0)
            setRGB(0,200,64)
            setText("Welcome to Smart Park capsule")
            setRGB(0,128,64)
            
        else:
            print("Door is close")
            #setText("Parking spots \n full!")
            #setRGB(0,10,64)
    

def ultra_actuation(ultra_output):
    if ultra_output is not None:
        if ultra_output == '(spotoccupied':
            print("occupied: led off")
            digitalWrite(led,0)
            #count_flag=1
            #notmax=0
            #GPIO.output(LED_PIN, True)
        else:
            print("Not occupied: led on")
            digitalWrite(led,1)        # Send HIGH to switch on LED
            #print ("LED ON!")
            #notmax=1
            

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
    prevTemp=26.0
    prevHumid =50.0 
    setText("Welcome to Smart Park capsule")
    setRGB(0,128,64)
    while 1:
        
        
        sleep(5)
        if connflag == True:
            timeStamp = datetime.datetime.now()
            tempreading = uniform(20.0,25.0)
        
        # Generating Temperature Readings
            [temperature, humidity] = grovepi.dht(TempPort, TempSensor)
            
            if math.isnan(temperature)== True or math.isnan(humidity)== True:
                temperature = prevTemp
                humidity = prevHumid
            else:
                prevTemp = temperature
                prevHumid = humidity
                
        # Generating Ultrasonic Readings
            us= grovepi.ultrasonicRead(Ultrasonic_ranger)
            us2= grovepi.ultrasonicRead(Ultrasonic_ranger2)
        # Generating Lightsensor Readings
            light= grovepi.analogRead(LightSensor)
        # Calculate resistance of sensor in K
            if light is not 0 :
                resistance = (float)(1024 - light) * 10 / light
            else :
                resistance = 1
     
           
        # Generating the IR sensor readings   
            IR_value = IR()
            message = '{"timeStamp":'+'"'+str(timeStamp)+'",'+'"temperature":'+str(temperature)+','+'"humidity":'+str(humidity) +','+'"Ultrasonic-1":'+str(us)+','+'"Ultrasonic-2":'+str(us2)+','+'"Lightsensor":'+str(light) +','+'"Light_resistance":'+str(resistance) +','+'"IR_sensor":'+str(IR_value) + '}'
            mqttc.publish("temperatureTopic", message, 1)        # topic: temperature # Publishing Temperature values
            client.publish("temperatureTopic", message, 1)  
            print("msg sent: temperature " + "%.1f" % temperature +" , humidity " + "%.1f" % humidity +", Ultrasonic-1 " + "%.1f" % us +", Ultrasonic-2 " + "%.1f" % us2 +", Lightsensor :" + "%.1f" % light  +", IR_sensor:  " + "%.1f" % IR_value   ) # Print sent temperature msg on console
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