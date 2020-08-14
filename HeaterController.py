import datetime
import logging
import math

HIGH = 22
LOW = 16
MIDDLE = (HIGH + LOW) / 2
HIGH_HOUR = 14
PRECISION = 0.5

class HeaterController:
    def __init__(self, heater, temperature, graphite):
        self.heater = heater
        self.temperature = temperature
        self.graphite = graphite
        self.started = False

    async def __call__(self):
        time = datetime.datetime.now().time()
        hour = time.hour + time.minute / 60
        target = math.cos((hour - HIGH_HOUR) / 24 * 2 * math.pi) * (HIGH - MIDDLE) + MIDDLE
        temperature = await self.temperature.temperature()
        logging.info("Temperature for heater is {}".format(temperature))
        logging.info("target temperature for heater is {}".format(target))
        if temperature < target - PRECISION:
            logging.info("Temperature < target - eps, starting heater")
            self.started = True
        if temperature > target + PRECISION:
            logging.info("Temperature > target + eps, stopping heater")
            self.started = False
        if self.started:
            await self.heater.start()
        else:
            await self.heater.stop()
        await self.graphite.send("heater", 1 if self.started else 0)
        await self.graphite.send("heater_target", target)

    def delay(self):
        return 30

