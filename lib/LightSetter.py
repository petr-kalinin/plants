import os
import sys
from pyA20.gpio import gpio
from pyA20.gpio import port

leds = (port.PA6, port.PA11, port.PA12)

gpio.init()
for led in leds:
    gpio.setcfg(led, gpio.OUTPUT)

if not os.getegid() == 0:
    sys.exit('Script must be run as root')

class LightSetter:
    async def set(self, *values):
        assert(len(values) == len(leds))
        for i in range(len(leds)):
            gpio.output(leds[i], 0 if values[i] else 1) 
