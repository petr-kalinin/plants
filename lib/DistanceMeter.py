import asyncio
import time
import os
from pyA20.gpio import gpio
from pyA20.gpio import port

trigPin = port.PA10
echoPin = port.PA14

v = 331.5+0.6*20

gpio.init()
gpio.setcfg(trigPin, gpio.OUTPUT)
gpio.setcfg(echoPin, gpio.INPUT)

if not os.getegid() == 0:
    sys.exit('Script must be run as root')

class DistanceMeter:
    async def __call__(self):
        gpio.output(trigPin, 0)
        time.sleep(0.5)

        gpio.output(trigPin, 1)
        time.sleep(1/1000000.0)
        gpio.output(trigPin, 0)
    
        start = time.time()
        while (gpio.input(echoPin) == 0 and time.time() < start + 1):
            pass
        start = time.time()
        while (gpio.input(echoPin) == 1 and time.time() < start + 1):
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
