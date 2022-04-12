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
        needed_len = get_boundary(SUMMER_LEN, WINTER_LEN)
        end_time = self.sun.sunrise() + datetime.timedelta(seconds=needed_len)
        start_time = self.sun.sunset() - datetime.timedelta(hours=1)
        logging.info("start={}, end={}, needed_len={} min".format(start_time, end_time, needed_len/60))
        now = datetime.datetime.now()
        value = now >= start_time and now <= end_time
        await self.graphite.send("light_sun", int(value))
        values = []
        for i in range(3):
            values.append(value)
            logging.info("value for light {} is {}".format(i, values[-1]))
        await self.setter.set(*values)

    def delay(self):
        return 60

