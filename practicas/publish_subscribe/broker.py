#!/usr/bin/env python

import subprocess

"""
    Starting mosquitto broker
    The mosquitto broker is going to help us to manage the communication between 
    the publisher and the subscriber and controlling the topics
"""

subprocess.run(["mosquitto"])
