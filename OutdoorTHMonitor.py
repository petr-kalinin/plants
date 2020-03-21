import asyncio
import logging

class OutdoorTHMonitor:
    def __init__(self, rtl433, graphite):
        self.rtl433 = rtl433
        self.graphite = graphite

    async def __call__(self):
        try:
            await self.rtl433.update()
            t = self.rtl433.temperature()
            rh = self.rtl433.humidity()
            if t is None or rh is None:
                return
            await asyncio.gather(
                self.graphite.send('outdoor_temperature', t),
                self.graphite.send('outdoor_humidity', rh))
        except Exception as e:
            logging.error("Could not read RTL433: " + str(e))

    def delay(self):
        return self.graphite.delay()
