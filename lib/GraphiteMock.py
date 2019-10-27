import logging
import asyncio

class Graphite:
    def __init__(self, host):
        logging.info("Init graphite {}".format(host))

    async def send(self, param, value):
        logging.info("Send: {} {}".format(param, value))
        await asyncio.sleep(1)

    def delay(self):
        return 20