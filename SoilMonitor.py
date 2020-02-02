import asyncio

class SoilMonitor:
    def __init__(self, soil, graphite):
        self.soil = soil
        self.graphite = graphite

    async def __call__(self):
        data = await self.soil()
        for i, h in enumerate(data):
            await self.graphite.send('soil.{}'.format(i), h)

    def delay(self):
        return self.graphite.delay()
