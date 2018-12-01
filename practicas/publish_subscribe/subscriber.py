#!/usr/bin/env python

import paho.mqtt.client as mqtt #import the client1

def on_connect(client, userdata, flags, rc):
    """
        This function prints the CONNACK response from
        the mosquitto broker
    """
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    """
        This function is the recommended to print the messages
        after received a callback
    """
    print("Topic: " + msg.topic + " Message: " + str(msg.payload)[1:])
    talk = open("messages.txt",'a')
    talk.write("Topic: " + msg.topic + " Message: " + str(msg.payload)[1:] + "\n")
    talk.close()

talk = open("messages.txt", 'w')
talk.close()
broker_address="192.168.8.5" 
client = mqtt.Client("salbot") #create new instance
client.on_message = on_message
client.connect(broker_address) #connect to broker
client.subscribe("distribuidos")

client.loop_forever()
