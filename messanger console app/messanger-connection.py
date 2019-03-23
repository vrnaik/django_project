#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import os


if __name__ == "__main__":
    broker="localhost"
    port=1883
    client = mqtt.Client()
    client.connect(broker, port)

    while True :
        client.loop()
        
        
        
        
        
        
        
        
        
        