import logging
import os
import sys
try:
    from pyA20.gpio import gpio
    from pyA20.gpio import port

    led = port.PA7

    gpio.init()
    gpio.setcfg(led, gpio.OUTPUT)

    if not os.getegid() == 0:
        sys.exit('Script must be run as root')
except ModuleNotFoundError:
    pass

class Heater:
    def __init__(self):
        gpio.output(led, 0)

    async def start(self):
        logging.info("Heater started!")
        gpio.output(led, 1)

    async def stop(self):
        logging.info("Heater stopped!")
        gpio.output(led, 0)
