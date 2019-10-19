#!/usr/bin/python3 -u
import time
from LightSetter import LightSetter
from SHT20 import SHT20

light_setter = LightSetter()
sht20 = SHT20()

while True:
    light_setter()
    sht20()
    time.sleep(60)