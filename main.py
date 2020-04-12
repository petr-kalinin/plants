#!/usr/bin/python3.8 -u
import asyncio
import logging

from Timer import Timer

from DistanceMonitor import DistanceMonitor
from LightController import LightController
from THMonitor import THMonitor
from OutdoorTHMonitor import OutdoorTHMonitor
from WaterLevelMonitor import WaterLevelMonitor
from PumpController import PumpController
from SoilMonitor import SoilMonitor

from config import is_mock, graphite_instance, soils
import config

if is_mock:
    from lib.LightSetterMock import LightSetter
    from lib.GraphiteMock import Graphite
    from lib.SHT20Mock import SHT20
    from lib.WaterLevelMock import WaterLevel
    from lib.WaterPumpMock import WaterPump
    from lib.SoilHumidityMock import SoilHumidity
else:
    from lib.LightSetter import LightSetter
    from lib.Graphite import Graphite
    from lib.SHT20 import SHT20
    from lib.RTL433 import RTL433
    from lib.WaterLevel import WaterLevel
    from lib.WaterPump import WaterPump
    from lib.SoilHumidity import SoilHumidity
    from lib.DistanceMeter import DistanceMeter

logging.basicConfig(format='%(asctime)s:%(filename)s:%(lineno)d: %(message)s', level=logging.DEBUG)

graphite = Graphite("ije.algoprog.ru", "plants." + str(graphite_instance))
sht20 = SHT20()
rtl433 = RTL433()
light_setter = LightSetter()
level = WaterLevel()
pump = WaterPump()
soil = SoilHumidity(0x48, [i for i in range(soils)])
distance = DistanceMeter()

monitor = Timer(THMonitor(sht20, graphite))
outdoor_monitor = Timer(OutdoorTHMonitor(rtl433, graphite))
light_controller = Timer(LightController(light_setter))
level_monitor = Timer(WaterLevelMonitor(level, graphite))
pump_controller = Timer(PumpController(level, pump, graphite), enabled=config.pump)
soil_monitor = Timer(SoilMonitor(soil, graphite))
distance_monitor = Timer(DistanceMonitor(distance, graphite), enabled=config.distance)

async def all():
    while True:
        await asyncio.gather(
            light_controller(),
            monitor(),
            outdoor_monitor(),
            level_monitor(),
            soil_monitor(),
            distance_monitor()
        )
        await asyncio.sleep(0.5)

async def pumper():
    while True:
        await pump_controller()
        await asyncio.sleep(0.5)

async def main():
    await asyncio.gather(all(), pumper())

asyncio.run(main())
