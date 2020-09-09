import asyncio

class LightnessMonitor:
    def __init__(self, lightness, graphite):
        self.lightness = lightness
        self.graphite = graphite

    async def __call__(self):
        try:
            data = await self.lightness()
            for i, h in enumerate(data):
                await self.graphite.send('lightness.{}'.format(i), h)
        except:
            print("Can't read lightness")
            pass

    def delay(self):
        return self.graphite.delay()
