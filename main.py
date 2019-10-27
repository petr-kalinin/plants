#!/usr/bin/python3 -u
import time
import logging

from Timer import Timer

from LightController import LightController
from THMonitor import THMonitor
from WaterLevelMonitor import WaterLevelMonitor
from PumpController import PumpController

from lib.LightSetterMock import LightSetter
from lib.GraphiteMock import Graphite
from lib.SHT20Mock import SHT20
from lib.WaterLevelMock import WaterLevel
from lib.WaterPumpMock import WaterPump

logging.basicConfig(format='%(asctime)s:%(filename)s:%(lineno)d: %(message)s', level=logging.INFO)

graphite = Graphite("ije.algoprog.ru")
sht20 = SHT20()
light_setter = LightSetter()
level = WaterLevel()
pump = WaterPump()

monitor = Timer(THMonitor(sht20, graphite))
light_controller = Timer(LightController(light_setter))
level_monitor = Timer(WaterLevelMonitor(level, graphite))
pump_controller = Timer(PumpController(level, pump, graphite))

while True:
    light_controller()
    monitor()
    level_monitor()
    pump_controller()
    time.sleep(0.5)