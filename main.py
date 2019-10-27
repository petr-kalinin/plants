#!/usr/bin/python3 -u
import asyncio
import logging

from Timer import Timer

from LightController import LightController
from THMonitor import THMonitor
from WaterLevelMonitor import WaterLevelMonitor
from PumpController import PumpController

from is_mock import is_mock

if is_mock:
    from lib.LightSetterMock import LightSetter
    from lib.GraphiteMock import Graphite
    from lib.SHT20Mock import SHT20
    from lib.WaterLevelMock import WaterLevel
    from lib.WaterPumpMock import WaterPump

logging.basicConfig(format='%(asctime)s:%(filename)s:%(lineno)d: %(message)s', level=logging.DEBUG)

graphite = Graphite("ije.algoprog.ru")
sht20 = SHT20()
light_setter = LightSetter()
level = WaterLevel()
pump = WaterPump()

monitor = Timer(THMonitor(sht20, graphite))
light_controller = Timer(LightController(light_setter))
level_monitor = Timer(WaterLevelMonitor(level, graphite))
pump_controller = Timer(PumpController(level, pump, graphite))

async def all():
    while True:
        await asyncio.gather(
            light_controller(),
            monitor(),
            level_monitor(),
        )
        await asyncio.sleep(0.5)

async def pumper():
    while True:
        await pump_controller()
        await asyncio.sleep(0.5)

async def main():
    await asyncio.gather(all(), pumper())

asyncio.run(main())