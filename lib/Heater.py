import logging
import os
import sys
try:
    from pyA20.gpio import gpio
    from pyA20.gpio import port

    leds = [port.PG7, port.PA2]

    gpio.init()
    for led in leds:
        gpio.setcfg(led, gpio.OUTPUT)

    if not os.getegid() == 0:
        sys.exit('Script must be run as root')
except ModuleNotFoundError:
    pass

class Heater:
    # For our relay the values are inverted
    def __init__(self):
        for led in leds:
            gpio.output(led, 1)

    async def start(self, i):
        logging.info("Heater {} started!".format(i))
        gpio.output(leds[i], 0)

    async def stop(self, i):
        logging.info("Heater {} stopped!".format(i))
        gpio.output(leds[i], 1)
