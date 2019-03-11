#!/usr/bin/env python3
# this sends the req to run the appliances and listen to check if the req is fulfilled
import paho.mqtt.client as mqtt
import json
# Server2
def on_connect(client, userdata, flags, rc):
    # print("Connected with result code "+str(rc))
    client.subscribe("topic/reqStatus")


def on_message(client, userdata, msg):
    if msg.topic == "topic/reqStatus":

        print('server2: message received on '+msg.topic)
        if msg.payload.decode() == "not fullfilled":
            print("server1: request cannot be fullfilled ")
            print("server2: sending user request again ")
            task1(client)
        else:
            print("server1: request is fulfilled ")
        # print(msg.payload.decode())print('--------------------------------')

        print('server2: waiting for reply from server1 ')
        # print(msg.payload)
        client.disconnect()


def task(client):
    # MQTT_MSG=json.dumps()
    client.connect("localhost", 1883, 60)
    client.publish("topic/userReq", MQTT_MSG)
    client.disconnect()
    print('--------------------------------')
    print('server2: user request is sent to server1 ')



def task1(client):
    # MQTT_MSG=json.dumps()
    client.connect("localhost", 1883, 60)
    client.publish("topic/userReq", json.dumps({"fan": {"id": "100", "status": "idle", "action": "start", "duration": "0", "startTime": "2:30", "stopTime": "3:30"}, "pump": {"id": "100", "status": "idle", "action": "start", "duration": "60", "startTime": "2:30", "stopTime": "3:30"}, "sprinkler": {"id": "100", "status": "idle", "action": "start", "duration": "60", "startTime": "2:30", "stopTime": "3:30"}, "light": {"id": "100", "status": "idle", "action": "start", "duration": "0", "startTime": "2:30", "stopTime": "3:30"}}))
    client.disconnect()


def listen(client):
    while True:
        client.connect("localhost", 1883, 60)
        client.on_connect = on_connect
        client.on_message = on_message
        print('--------------------------------')

        print('server2: waiting for reply from server1 ')
        client.loop_forever()
        # print('waiting for result.....')


if __name__ == "__main__":
    MQTT_MSG = json.dumps({"fan": {"id": "100", "status": "idle", "action": "start", "duration": "60", "startTime": "2:30", "stopTime": "3:30"}, "pump": {"id": "100", "status": "idle", "action": "start", "duration": "60", "startTime": "2:30", "stopTime": "3:30"}, "sprinkler": {"id": "100", "status": "idle", "action": "start", "duration": "60", "startTime": "2:30", "stopTime": "3:30"}, "light": {"id": "100", "status": "idle", "action": "start", "duration": "60", "startTime": "2:30", "stopTime": "3:30"}})
    client = mqtt.Client()
    task(client)
    listen(client)

