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
        daytime = self.sun.sunset() - self.sun.sunrise()
        offset = (12 * 60 * 60 - daytime.total_seconds()) / 4
        summer_len = SUMMER_LEN + offset
        needed_len = get_boundary(summer_len, WINTER_LEN)
        end_time = self.sun.sunrise() + datetime.timedelta(seconds=needed_len)
        start_time = self.sun.sunset() - datetime.timedelta(seconds=(60 * 60 + offset))
        logging.info("start={}, end={}, needed_len={} min".format(start_time, end_time, needed_len/60))
        now = datetime.datetime.now()
        day_start = datetime.datetime.combine(datetime.date.today(), datetime.time(0))
        value = now >= start_time and now <= end_time
        await self.graphite.send("light_sun", int(value))
        await self.graphite.send("light_sun_needed_len", needed_len)
        await self.graphite.send("light_sun_start_time", (start_time - day_start).total_seconds())
        await self.graphite.send("light_sun_end_time", (end_time - day_start).total_seconds())
        await self.graphite.send("light_sun_sunrise", (self.sun.sunrise() - day_start).total_seconds())
        await self.graphite.send("light_sun_sunset", (self.sun.sunset() - day_start).total_seconds())
        if end_time > start_time:
            await self.graphite.send("light_sun_duration", (end_time - start_time).total_seconds())
        await self.graphite.send("light_sun_daytime", daytime.total_seconds())
        values = []
        for i in range(3):
            values.append(value)
            logging.info("value for light {} is {}".format(i, values[-1]))
        await self.setter.set(*values)

    def delay(self):
        return 60

