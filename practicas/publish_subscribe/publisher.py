#!/usr/bin/env python

import paho.mqtt.client as mqtt 
import time
import sys

broker_address="localhost"
client = mqtt.Client("pops") 
client.connect(broker_address)
client.publish("distribuidos", str(sys.argv[1]))
time.sleep(1)
