#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import os
qos = 1
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)
    client.subscribe("topic/test", session, qos)
   
   
def on_message(client, userdata, msg):
    if msg.topic == "topic/test":        
        print(msg.payload.decode())

if __name__ == "__main__":
    broker="localhost"
    port=1883
    duration=8000
    session = False
    client = mqtt.Client()

    os.system('clear')
    client.connect(broker, port, duration)
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop()
    cstr = 'Message Display'
#     print('\t\t Message Display')
    print (cstr.center(50, '='))
    while True :
        

        client.loop()
        
        
        
        
        
        
        
        
        
        