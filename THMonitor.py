import asyncio
import logging

class THMonitor:
    def __init__(self, sht20, graphite):
        self.sht20 = sht20
        self.graphite = graphite

    async def __call__(self):
        try:
            t, rh = await asyncio.gather(
                self.sht20.temperature(),
                self.sht20.humidity())
            await asyncio.gather(
                self.graphite.send('plants.temperature', t),
                self.graphite.send('plants.humidity', rh))
        except Exception as e:
            logging.error("Could not read SHT20: " + str(e))

    def delay(self):
        return self.graphite.delay()
