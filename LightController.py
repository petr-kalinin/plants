import datetime
import logging

on_periods = ((datetime.time(6, 0), datetime.time(22, 0)),
              (datetime.time(6, 0), datetime.time(22, 0)),
              (datetime.time(6, 0), datetime.time(22, 0)))

class LightController:
    def __init__(self, setter):
        self.setter = setter

    async def __call__(self):
        time = datetime.datetime.now().time()
        values = []
        for i in range(3):
            values.append(time > on_periods[i][0] and time < on_periods[i][1])
            logging.info("value for light {} is {}".format(i, values[-1]))
        await self.setter.set(*values)

    def delay(self):
        return 60

