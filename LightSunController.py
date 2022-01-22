import datetime
import logging
from HeaterController import get_boundary

SUMMER_LEN = 12 * 60 * 60
WINTER_LEN = 9 * 60 * 60

class LightSunController:
    def __init__(self, setter, sun, graphite):
        self.setter = setter
        self.sun = sun
        self.graphite = graphite

    async def __call__(self):
        daylength = self.sun.daylength().seconds
        needed_len = get_boundary(SUMMER_LEN, WINTER_LEN)
        delta = datetime.datetime.now() - self.sun.sunset()
        logging.info("daylength={} min, needed_len={} min".format(daylength/60, needed_len/60))
        value = False
        if needed_len > daylength:
            last_delta = needed_len - daylength
            logging.info("last_delta={} min, now_delta={}".format(last_delta/60, delta.seconds/60))
            value = delta > datetime.timedelta(hours=-1) and delta < datetime.timedelta(seconds=last_delta)
        await self.graphite.send("light_sun", int(value))
        values = []
        for i in range(3):
            values.append(value)
            logging.info("value for light {} is {}".format(i, values[-1]))
        await self.setter.set(*values)

    def delay(self):
        return 60

