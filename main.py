#!/usr/bin/python3 -u
import time
from LightSetter import LightSetter

light_setter = LightSetter()

while True:
    light_setter()
    time.sleep(60)