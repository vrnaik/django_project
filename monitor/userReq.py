#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import sys, os
# This is the Publisher
#MQTT_MSG=json.dumps({"fan": "1","pump":  "2","light": "1","sprinkler":  "3"});
#below MQTT_MSG is what i was using
# MQTT_MSG=json.dumps({"fan":{"id":"100","status":"idle","action":"start","duration":"60","startTime":"2:30","stopTime":"3:30"},"pump":{"id":"100","status":"idle","action":"start","duration":"60","startTime":"2:30","stopTime":"3:30"},"sprinkler":{"id":"100","status":"idle","action":"start","duration":"60","startTime":"2:30","stopTime":"3:30"},"light":{"id":"100","status":"idle","action":"start","duration":"60","startTime":"2:30","stopTime":"3:30"}});

host = 'localhost'
port = 1883
duration = 8000

dat = sys.stdin.read()

# data = bytes.decode(dat)

# sys.stdout.write('Received: %s'%dat)

def binary_to_dict(the_binary):
    jsn = ''.join(chr(int(x, 2)) for x in the_binary.split())
    d = json.loads(jsn)
    return d

def on_connect(client, userdata, flags, rc):
  #print("Connected with result code "+str(rc))
  client.subscribe("topic/reqStatus")
  # client.subscribe("topic/userReq")
  # client.subscribe("topic/generated")
  # client.subscribe("topic/statusA")
  # client.subscribe("topic/statusR")

def on_message(client, userdata, msg):
    #if msg.payload.decode() == "Hello world!":
    if msg.topic == "topic/reqStatus" :
        # print(msg.payload.decode())
        sys.stdout.write('server2: message received on '+msg.topic)
        if msg.payload.decode() == "not fullfilled":
            sys.stdout.write("server1: sufficient amount of resource is not available ")
            sys.stdout.write("server1: the request cannot be fullfilled ")
            # print("server2: sending user request again ")
            sys.stdout.write("server1: remove some less priority items and try again")
            client.disconnect()
            exit(0)
        else:
            sys.stdout.write("server1: request is fulfilled ")
            client.disconnect()
            exit(0)
        # print(msg.payload.decode())
        # print(msg.payload)
        client.disconnect()


def connection(client):
    client.connect(host, port, duration)
    client.on_connect = on_connect
    client.on_message = on_message
    return client

def sendReq(client):

    # with open('/home/vikas/project/viki/file.json') as f:
    #     data = json.load(f)
    #     f.close()
    data = binary_to_dict(dat)
    MQTT_MSG=json.dumps({"fan":{"id":"100","status":data['status'],"action":data['action'],"duration":data['duration'],"startTime":data['startTime'],"stopTime":data['stopTime']},"pump":{"id":"100","status":data['status1'],"action":data['action1'],"duration":data['duration1'],"startTime":data['startTime1'],"stopTime":data['stopTime1']},"sprinkler":{"id":"100","status":data['status2'],"action":data['action2'],"duration":data['duration2'],"startTime":data['startTime2'],"stopTime":data['stopTime2']},"light":{"id":"100","status":data['status3'],"action":data['action3'],"duration":data['duration3'],"startTime":data['startTime3'],"stopTime":data['stopTime3']}});
    # MQTT_MSG=json.dumps({"fan":{"id":"100","status":data['status'],"action":data['action'],"duration":data['duration'],"startTime":data['startTime'],"stopTime":data['stopTime']}})
    
    client = connection(client)

    client.publish("topic/userReq", MQTT_MSG)
    client.disconnect()
    # print('--------------------------------')
    sys.stdout.write('server2: user request is sent to server1 ')


def listen(client):

    # print('--------------------------------')
    sys.stdout.write('server2: waiting for reply from server1 ')
#     client = connection(client)
  
    while True:
        client.connect("localhost", 1883)
        client.on_connect = on_connect
        client.on_message = on_message

        client.loop_forever()
        # print('waiting for result.....')


if __name__ == "__main__":
    #fan-0,pump-1, sprinkler-3, light-3
      # MQTT_MSG=json.dumps({"fan":{"id":"100","status":data['status'],"action":data['action'],"duration":data['duration'],"startTime":data['startTime'],"stopTime":data['stopTime']},"pump":{"id":"100","status":data['status1'],"action":data['action1'],"duration":data['duration1'],"startTime":data['startTime1'],"stopTime":data['stopTime1']}});
    # print(MQTT_MSG)
    client = mqtt.Client()
    # while True:
    sendReq(client)
    listen(client)





















