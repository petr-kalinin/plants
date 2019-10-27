import os
import sys
from pyA20.gpio import gpio
from pyA20.gpio import port

led = port.PA7

gpio.init()
gpio.setcfg(led, gpio.INPUT)

if not os.getegid() == 0:
    sys.exit('Script must be run as root')

class WaterLevel:
    async def __call__(self):
        return gpio.input(led)
