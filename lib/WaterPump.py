import logging
import os
import sys
from pyA20.gpio import gpio
from pyA20.gpio import port

led = port.PA2

gpio.init()
gpio.setcfg(led, gpio.OUTPUT)

if not os.getegid() == 0:
    sys.exit('Script must be run as root')

class WaterPump:
    def __init__(self):
        gpio.output(led, 1)

    async def start(self):
        logging.info("Pump started!")
        gpio.output(led, 0)

    async def stop(self):
        logging.info("Pump stopped!")
        gpio.output(led, 1)
