from .ads.ads1115 import ADS1115

class SoilHumidity:
    def __init__(self, address, channel):
        self.ads = ADS1115(1, address=address)
        self.channel = channel

    async def __call__(self):
        return self.ads.read(self.channel)
    