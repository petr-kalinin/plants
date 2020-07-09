import asyncio

class Ping:
    def __init__(self, graphite):
        self.graphite = graphite

    async def __call__(self):
        await self.graphite.send('ping', 1)

    def delay(self):
        return self.graphite.delay()
