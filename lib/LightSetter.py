import os
import sys
try:
    from pyA20.gpio import gpio
    from pyA20.gpio import port

    leds = [(port.PA6, port.PA11, port.PA12), (port.PA0, port.PA11, port.PA12)]

    if not os.getegid() == 0:
        sys.exit('Script must be run as root')
except ModuleNotFoundError:
    pass


class LightSetter:
    def __init__(self, pinset=0):
        self._initialized = False
        self.pinset = pinset

    async def set(self, *values):
        if not self._initialized:
            gpio.init()
            for led in leds[self.pinset]:
                gpio.setcfg(led, gpio.OUTPUT)
            self._initialized = True
        assert(len(values) == len(leds[self.pinset]))
        for i in range(len(leds[self.pinset])):
            gpio.output(leds[self.pinset][i], 0 if values[i] else 1) 
