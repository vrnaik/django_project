#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import os
qos = 1
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)
       
def pub(client, name):
    ms = input('\ntype message: ')
    client.publish("topic/test", name+': '+str(ms), qos);

if __name__ == "__main__":
    broker="localhost"
    port=1883
    duration=8000
    session = False
    
    client = mqtt.Client()

    os.system('clear')
    client.connect(broker, port, duration)
    client.on_connect = on_connect
    client.loop()
    
    cstr = 'Type message'
#     print('\t\t Type message')
    print (cstr.center(50, '='))
    name = input('\nyour name: ')
    while True :
#         client.on_connect = on_connect
        client.loop()
        pub(client, name) 
        
        
        
