#!/usr/bin/python3.8 -u
import asyncio
import logging

from Timer import Timer

from DistanceMonitor import DistanceMonitor
from LightController import LightController
from LightSunController import LightSunController
from THMonitor import THMonitor
from OutdoorTHMonitor import OutdoorTHMonitor
from WaterLevelMonitor import WaterLevelMonitor
from PumpController import PumpController
from SoilMonitor import SoilMonitor
from LightnessMonitor import LightnessMonitor
from Ping import Ping
from HeaterController import HeaterController
from DachaPumpController import DachaPumpController

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
    from lib.Lightness import Lightness
    from lib.Graphite import Graphite
    from lib.SHT20 import SHT20
    from lib.RTL433 import RTL433
    from lib.WaterLevel import WaterLevel
    from lib.WaterPump import WaterPump
    from lib.SoilHumidity import SoilHumidity
    from lib.DistanceMeter import DistanceMeter
    from lib.Heater import Heater
    from lib.Display import Display
    from lib.Joystick import Joystick
    from lib.Sun import Sun

logging.basicConfig(format='%(asctime)s:%(filename)s:%(lineno)d: %(message)s', level=logging.DEBUG)

graphite = Graphite("ije.algoprog.ru", "plants." + str(graphite_instance), config.graphite_attempts)
sht20 = SHT20(bus=config.i2c) if config.th_monitor else None
rtl433 = RTL433() if config.rtl433 else None
light_setter = LightSetter() if config.light or config.light_sun else None
level = WaterLevel(config.invert_level) if config.level else None
pump = WaterPump() if config.pump else None
soil = SoilHumidity(0x48, [i for i in range(soils)]) if config.soils > 0 else None
lightness = Lightness(0x48, config.lightness) if config.lightness else None
distance = DistanceMeter() if config.distance else None
heater = Heater() if config.heater else None
display = Display(config.i2c) if config.display else None
joystick = Joystick(0x48, [0, 1]) if config.joystick else None
sun = Sun() if config.light_sun else None

monitor = Timer(THMonitor(sht20, graphite), enabled=config.th_monitor)
outdoor_monitor = Timer(OutdoorTHMonitor(rtl433, graphite), enabled=config.rtl433)
light_controller = Timer(LightController(light_setter), enabled=config.light)
light_sun_controller = Timer(LightSunController(light_setter, sun, graphite), enabled=config.light_sun)
level_monitor = Timer(WaterLevelMonitor(level, graphite), enabled=config.level)
pump_controller = Timer(PumpController(level, pump, graphite), enabled=config.pump)
soil_monitor = Timer(SoilMonitor(soil, graphite), enabled=config.soils > 0)
distance_monitor = Timer(DistanceMonitor(distance, graphite), enabled=config.distance)
lightness_monitor = Timer(LightnessMonitor(lightness, graphite), enabled=len(config.lightness)>0)
ping = Timer(Ping(graphite), enabled=config.ping)
heater_controller = Timer(HeaterController(heater, sht20, display, joystick, graphite, config.heater_t_max), enabled=config.heater)
dacha_pump_controller = Timer(DachaPumpController(distance, pump, graphite), enabled=config.dacha_pump)

async def all():
    while True:
        await asyncio.gather(
            light_controller(),
            light_sun_controller(),
            monitor(),
            outdoor_monitor(),
            level_monitor(),
            soil_monitor(),
            distance_monitor(),
            lightness_monitor(),
            ping(),
            heater_controller(),
        )
        await asyncio.sleep(0.5)

async def pumper():
    while True:
        await asyncio.gather(
            pump_controller(),
            dacha_pump_controller()
        )
        await asyncio.sleep(0.5)

async def main():
    await asyncio.gather(all(), pumper())

asyncio.run(main())
