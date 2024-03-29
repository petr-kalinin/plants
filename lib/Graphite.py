import asyncio
from aiographite import connect
from aiographite.protocol import PlaintextProtocol
import logging

class Graphite:
    def __init__(self, host, prefix, attempts):
        self.connection = None
        self.host = host
        self.prefix = prefix
        self.attempts = attempts

    async def send(self, param, value):
        param = self.prefix + "." + param
        for i in range(self.attempts):
            try:
                logging.info("Send: {} {} attempt {}".format(param, value, i))
                if not self.connection:
                    self.connection = await connect(self.host)
                await self.connection.send(param, value)
                break
            except Exception as e:
                logging.info("Can't send: {} {} attempt {}: {}".format(param, value, i, e))
                await asyncio.sleep((2 ** i) / 10)

    def delay(self):
        return 20
