import os
import sys
try:
    from pyA20.gpio import gpio
    from pyA20.gpio import port

    leds = [port.PA11]

    if not os.getegid() == 0:
        sys.exit('Script must be run as root')
except ModuleNotFoundError:
    pass


class LightSetter:
    def __init__(self):
        self._initialized = False

    async def set(self, *values):
        if not self._initialized:
            gpio.init()
            for led in leds:
                gpio.setcfg(led, gpio.OUTPUT)
            self._initialized = True
        assert(len(values) >= len(leds))
        for i in range(len(leds)):
            gpio.output(leds[i], 0 if values[i] else 1) 
