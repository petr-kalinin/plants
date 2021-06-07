import datetime
import logging
import math

# Note that distance is reversed: this is the distance from sensor to water,
# not the distance from water to bottom.
DISTANCE_FOR_OFF = 10
DISTANCE_FOR_ON = 30
MAX_PUMP_TIME = datetime.timedelta(seconds=60)
PERIOD_TIME = datetime.timedelta(minutes=15)

class DachaPumpController:
    def __init__(self, distance, pump, graphite):
        self.distance = distance
        self.pump = pump
        self.graphite = graphite
        self.start_time = None

    async def __call__(self):
        dist = await self.distance()
        now = datetime.datetime.now()
        if self.start_time and now - self.start_time > PERIOD_TIME:
            self.start_time = None
        if dist > DISTANCE_FOR_ON and not self.start_time:
            logging.info("Starting pump")
            self.start_time = now
        if dist < DISTANCE_FOR_OFF:
            logging.info("Stopping pump")
            self.start_time = None
        if self.start_time and now - self.start_time < MAX_PUMP_TIME:
            await self.pump.start()
        else:
            await self.pump.stop()
        await self.graphite.send("pump", 1 if self.start_time else 0)

    def delay(self):
        return 1
