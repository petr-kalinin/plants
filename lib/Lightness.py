from .ads.ads1115 import ADS1115

class Lightness:
    def __init__(self, address, channels):
        self.ads = ADS1115(1, address=address)
        self.channels = channels

    async def __call__(self):
        return [self.ads.read(channel) for channel in self.channels]
    