#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json, pickle
import subprocess
import os
import powerConsumption
# This is the Subscriber

# def availability():

# Server1
def processData(payload):
    fp = open("shareddata.pkl",'rb')
    value = pickle.load(fp)
    available = int(value['available'])
    # print(available)
    # print(type(available))
    duration = 0
    required = 0
    # available = 40000
    print(len(payload))
    print(list(payload.keys())[0])  # created list of payload keys

    for devices in list(payload.keys()):
        # print(x)
        # print(payload[x]["action"])
        if payload[devices]["action"] == "start":
            required = required+(int(payload[devices]["duration"])*watt[devices])
    if required > available:
        print("requirement cannot be fullfilled")
        client.publish("topic/reqStatus", "not fullfilled")
    else:

        print("successfull")
        client.publish("topic/reqStatus", "fullfilled")


def on_connect(client, userdata, flags, rc):
    # print("Connected with result code "+str(rc))
    client.subscribe("topic/test")
    client.subscribe("topic/userReq")
    client.subscribe("topic/generated")
    client.subscribe("topic/statusA")
    client.subscribe("topic/statusR")


def on_message(client, userdata, msg):
    # if msg.payload.decode() == "Hello world!":
    if msg.topic == "topic/test":
        print(msg.topic)
        print("its test topic")
        # print(msg.payload.decode())
        # print(msg.payload)
        client.disconnect()

    if msg.topic == "topic/userReq":
        print('server1: received message on '+msg.topic)
        # print(type(msg.payload.decode()))
        print(msg.payload.decode())  # msg.payload is of string type
        payload = json.loads(msg.payload)  # you can use json.loads to convert string to json(also called as dictionary in python)
        # print(type(payload))
        print(payload["fan"])  # then you can check the value
        processData(payload)
        # p = subprocess.Popen(['/bin/sh', os.path.expanduser('~/Desktop/sleeper.sh')])
        #
        # print(p.pid)

        client.disconnect()  # Got message then disconnect

    if msg.topic == "topic/generated":
        print(msg.topic)

    if msg.topic == "topic/statusA":
        print(msg.topic)

    if msg.topic == "topic/statusR":
        print(msg.topic)


if __name__ == "__main__":

    watt = {"fan": powerConsumption.FAN, "light": powerConsumption.LIGHT, "pump": powerConsumption.PUMP, "sprinkler": powerConsumption.SPRINKLER}  # in python we can write json data in dictionary
    # print(type(watt))
    client = mqtt.Client('www.viresor.com:1883')
    while True:
        client.connect("www.viresor.com", 1883, 60)
        client.on_connect = on_connect
        client.on_message = on_message
        print('server1 started..')
        client.loop_forever()



'''
import subprocess
import os
p = subprocess.Popen(['/bin/sh', os.path.expanduser('~/tmp/sleeper.sh')])
# look ma, no pipes!
print p.pid
# prints 29893
'''
