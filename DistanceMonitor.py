import asyncio

class DistanceMonitor:
    def __init__(self, distance, graphite):
        self.distance = distance
        self.graphite = graphite

    async def __call__(self):
        data = await self.distance()
        await self.graphite.send('distance', data)

    def delay(self):
        return self.graphite.delay()
