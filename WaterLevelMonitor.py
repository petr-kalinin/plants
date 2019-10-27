class WaterLevelMonitor:
    def __init__(self, level, graphite):
        self.level = level
        self.graphite = graphite

    async def __call__(self):
        await self.graphite.send("plants.waterlevel", await self.level())

    def delay(self):
        return self.graphite.delay()
