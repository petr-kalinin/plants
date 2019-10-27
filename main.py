#!/usr/bin/python3 -u
import time
from LightController import LightController
from THMonitor import THMonitor

from lib.LightSetterMock import LightSetter
from lib.GraphiteMock import Graphite
from lib.SHT20Mock import SHT20

graphite = Graphite("ije.algoprog.ru")
sht20 = SHT20()
light_setter = LightSetter()

monitor = THMonitor(sht20, graphite)
light_controller = LightController(light_setter)

while True:
    light_controller()
    monitor()
    time.sleep(60)