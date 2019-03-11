#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Publisher

client = mqtt.Client()
client.connect("www.viresor.com",1883,60)
client.publish("topic/test", "Hi, there!! whats going on");
client.disconnect();
