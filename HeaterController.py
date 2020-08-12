import datetime
import logging

class LightController:
    def __init__(self, heater, temperature, graphite):
        self.heater = heater
        self.temperature = temperature
        self.started = False

    async def __call__(self):
        time = datetime.datetime.now().time()
        temperature = await self.temperature.temperature()
        logiing.info("Temperature for heater is {}".format(temperatire)
        if temperature < 20:
            logging.info("Temperature < 20, starting heater")
            self.started = True
        if temperature > 21:
            logging.info("Temperature > 21, stopping heater")
            self.started = False
        if self.started:
            await self.heater.start()
        else:
            await self.heater.stop()
        await self.graphite.send("heater", 1 if self.started else 0)

    def delay(self):
        return 60

