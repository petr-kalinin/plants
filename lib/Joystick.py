#!/usr/bin/python3.8
import asyncio

try:
    from ads.ads1115 import ADS1115
except ModuleNotFoundError:
    pass

class Joystick:
    def __init__(self, address, channels):
        self.ads = ADS1115(1, address=address)
        self.channels = channels

    async def __call__(self):
        return [self.ads.read(channel) for channel in self.channels]

async def main():
    j = Joystick(0x48, [0, 1])
    while True:
        print(await j())
        sys.stdout.flush()
        await asyncio.sleep(0.3)

if __name__ == "__main__":
    asyncio.run(main())