#!/usr/bin/env python3
import paho.mqtt.client as mqtt



# This is the Subscriber

def on_connect(client, userdata, flags, rc):
    client.subscribe("topic/test")
   
   
def on_message(client, userdata, msg):
    if msg.topic == "topic/test":        
        print("\nreceived: "+msg.payload.decode())
        client.disconnect()

def pub():
    client = mqtt.Client()
    ms = input('\ntype message: ')
    client.connect(broker,port,60)
    client.publish("topic/test", str(ms));
    client.disconnect();
    wait()


def rep():
    client = mqtt.Client()
    client.connect(broker,port,60)
    client.publish("topic/test", 'hmm');
    client.disconnect();
    
def out():
    client = mqtt.Client()
    client.connect(broker,port,60)
    client.publish("topic/test", 'bye');
    client.disconnect();    
    
def wait():
    print('\nwaiting for reply')   
    client.loop_forever()       


#     www.viresor.com
if __name__ == "__main__":
    broker="localhost"
    port=1883

    client = mqtt.Client()

    while True:
        client.connect(broker, port, 60)
        client.on_connect = on_connect
        client.on_message = on_message
        
            
            
        a = input('\n y[send message ], n[nothing to say], o[over and out], s[start listening]: ')
        if a == 'y' :
            pub() 
        
        if a == 'n' :
            rep()
            
        if a == 'o' :
            out()    
            
        if a == 's' :
            print('\nserver is listening')    
            client.loop_forever()     
            
#         print('\nwaiting for reply')    
        client.loop_forever()




