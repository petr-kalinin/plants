import asyncio
import time
import os

v = 331.5+0.6*20

class DistanceMeter:
    def __init__(self):
        if os.getegid() != 0:
            raise PermissionError('Script must be run as root')

        from pyA20.gpio import gpio, port

        self.gpio = gpio
        self.trigPin = port.PA10
        self.echoPin = port.PA14
        gpio.init()
        gpio.setcfg(self.trigPin, gpio.OUTPUT)
        gpio.setcfg(self.echoPin, gpio.INPUT)

    async def __call__(self):
        self.gpio.output(self.trigPin, 0)
        time.sleep(0.5)

        self.gpio.output(self.trigPin, 1)
        time.sleep(1/1000000.0)
        self.gpio.output(self.trigPin, 0)
    
        start = time.time()
        while (self.gpio.input(self.echoPin) == 0 and time.time() < start + 1):
            pass
        start = time.time()
        while (self.gpio.input(self.echoPin) == 1 and time.time() < start + 1):
            pass
        end = time.time()
        t = end - start

        d = t * v * 100 / 2
        return d

async def main():
    meter = DistanceMeter()
    while True:
        d = await meter() 
        print("Distance: %.2f cm" % d)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
