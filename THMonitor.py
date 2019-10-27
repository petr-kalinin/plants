import asyncio

import logging

class THMonitor:
    def __init__(self, sht20, graphite):
        self.sht20 = sht20
        self.graphite = graphite

    async def __call__(self):
        t = await self.sht20.temperature()
        rh = await self.sht20.humidity()
        await self.graphite.send('plants.temperature', t)
        await self.graphite.send('plants.humidity', rh)

    def delay(self):
        return self.graphite.delay()
