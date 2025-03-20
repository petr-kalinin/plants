import logging
import os
import sys
try:
    from pyA20.gpio import gpio
    from pyA20.gpio import port

    LEDS = [port.PA2, port.PA11]

    gpio.init()
    for led in LEDS:
        gpio.setcfg(led, gpio.OUTPUT)

    if not os.getegid() == 0:
        sys.exit('Script must be run as root')
except ModuleNotFoundError:
    pass

class WaterPump:
    def __init__(self, idx):
        self.id = ids
        self.led = LEDS[idx]
        gpio.output(self.led, 1)

    async def start(self):
        logging.info("Pump started! " + str(self.id))
        gpio.output(self.led, 0)

    async def stop(self):
        logging.info("Pump stopped! " + str(self.id))
        gpio.output(self.led, 1)
