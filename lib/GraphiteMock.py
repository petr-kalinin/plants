import logging
import asyncio

class Graphite:
    def __init__(self, host, prefix):
        logging.info("Init graphite {}, {}".format(host, prefix))
        self.prefix = prefix

    async def send(self, param, value):
        param = self.prefix + "." + param
        logging.info("Send: {} {}".format(param, value))
        await asyncio.sleep(1)

    def delay(self):
        return 20
