#!/usr/bin/python3 -u
import time
from Timer import Timer

from LightController import LightController
from THMonitor import THMonitor
from WaterLevelMonitor import WaterLevelMonitor

from lib.LightSetterMock import LightSetter
from lib.GraphiteMock import Graphite
from lib.SHT20Mock import SHT20
from lib.WaterLevelMock import WaterLevel

graphite = Graphite("ije.algoprog.ru")
sht20 = SHT20()
light_setter = LightSetter()
level = WaterLevel()

monitor = Timer(THMonitor(sht20, graphite))
light_controller = Timer(LightController(light_setter))
level_monitor = Timer(WaterLevelMonitor(level, graphite))

while True:
    light_controller()
    monitor()
    level_monitor()
    time.sleep(0.5)