#!/usr/bin/env python3
import paho.mqtt.client as mqtt



# This is the Subscriber

def on_connect(client, userdata, flags, rc):
    client.subscribe("topic/test")
       
   
def on_message(client, userdata, msg):
    # if msg.payload.decode() == "Hello world!":
    if msg.topic == "topic/test":
        print(msg.topic)
        print(msg.payload.decode())
        print("its test topic")
        client.disconnect()

def pub():
    client = mqtt.Client()
    ms = input('type message')
    client.connect("www.viresor.com",1883,60)
    client.publish("topic/test", str(ms));
    client.disconnect();


#     www.viresor.com
if __name__ == "__main__":

    client = mqtt.Client("www.viresor.com", 1883, 60)
    while True:
        client.connect("www.viresor.com", 1883, 60)
        client.on_connect = on_connect
        client.on_message = on_message
        print('want to send message')
        a = input('want to send message type y otherwise n')
        if a == 'y' :
            pub()
        else:
            client.publish("topic/test", 'nothing to say');
            
        client.loop_forever()




