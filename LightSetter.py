import os
import sys
import datetime
from pyA20.gpio import gpio
from pyA20.gpio import port

leds = (port.PA6, port.PA11, port.PA12)
on_periods = ((datetime.time(6, 0), datetime.time(22, 0)),
              (datetime.time(6, 30), datetime.time(21, 30)),
              (datetime.time(7, 0), datetime.time(21, 0)))

gpio.init()
for led in leds:
    gpio.setcfg(led, gpio.OUTPUT)


if not os.getegid() == 0:
    sys.exit('Script must be run as root')


class LightSetter:
    def __call__(self):
        time = datetime.datetime.now().time()
        print("time=", time)
        for i in range(3):
            value = time > on_periods[i][0] and time < on_periods[i][1]
            print("value for light {} is {}".format(i, value))
            gpio.output(leds[i], 0 if value else 1) 

if __name__ == "__main__":
    LightSetter()()