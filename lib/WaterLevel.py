import asyncio
import os
import sys
try:
    from pyA20.gpio import gpio
    from pyA20.gpio import port

    led = port.PA7

    gpio.init()
    gpio.setcfg(led, gpio.INPUT)

    if not os.getegid() == 0:
        sys.exit('Script must be run as root')
except ModuleNotFoundError:
    pass

class WaterLevel:
    async def __call__(self):
        return 1 - gpio.input(led)

async def main():
    level = WaterLevel()
    while True:
        print(await level(), end="")
        sys.stdout.flush()
        await asyncio.sleep(0.3)

if __name__ == "__main__":
    asyncio.run(main())