import datetime
import logging
import math

"""
# Summer regime
HIGH = 23
LOW = 15
"""

# Winter regime
HIGH = 19
LOW = 8

MIDDLE = (HIGH + LOW) / 2
HIGH_HOUR = 15.5
DELTA = 1

def unscaled_target(phase):
    base = math.cos(phase)
    x = abs(base) ** (1/2)
    if base < 0:
        x = - x
    return x

class HeaterController:
    def __init__(self, heater, temperature, display, graphite):
        self.heater = heater
        self.temperature = temperature
        self.graphite = graphite
        self.display = display
        self.started = [False, False]

    async def __call__(self):
        time = datetime.datetime.now().time()
        hour = time.hour + time.minute / 60
        target = unscaled_target((hour - HIGH_HOUR) / 24 * 2 * math.pi) * (HIGH - MIDDLE) + MIDDLE
        temperature = await self.temperature.temperature()
        logging.info("Temperature for heater is {}".format(temperature))
        logging.info("target temperature for heater is {}".format(target))
        # heater 1
        if temperature < target:
            logging.info("Starting heater 1")
            self.started[0] = True
        if temperature > target + DELTA:
            logging.info("Stopping heater 1")
            self.started[0] = False
        # heater 2
        if temperature < target - DELTA:
            logging.info("Starting heater 2")
            self.started[1] = True
        if temperature > target:
            logging.info("Stopping heater 2")
            self.started[1] = False
        for i in range(2):
            if self.started[i]:
                await self.heater.start(i)
            else:
                await self.heater.stop(i)
        if self.display:
            self.display.print("%02d:%02d"% (time.hour, time.minute), 0)
            self.display.print("T=%2.1f" % temperature, 1)
            self.display.print("target=%2.1f" % target, 2)
            self.display.print("".join([" ON" if self.started[i] else "off" for i in range(2)]), 3)
        for i in range(2):
            await self.graphite.send("heater.{}".format(i), 1 if self.started[i] else 0)
        await self.graphite.send("heater_target", target)

    def delay(self):
        return 30

