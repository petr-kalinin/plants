import asyncio

class SoilMonitor:
    def __init__(self, soil, graphite):
        self.soil = soil
        self.graphite = graphite

    async def __call__(self):
        h = await self.soil()
        await self.graphite.send('plants.soil.0', h),

    def delay(self):
        return self.graphite.delay()
