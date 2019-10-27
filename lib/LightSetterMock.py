import logging

class LightSetter:
    async def set(self, *values):
        for i in range(len(values)):
            logging.info("Light {} = {}".format(i, values[i]))
