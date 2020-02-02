from aiographite import connect
from aiographite.protocol import PlaintextProtocol
import logging

class Graphite:
    def __init__(self, host, prefix):
        self.connection = None
        self.host = host
        self.prefix = prefix

    async def send(self, param, value):
        if not self.connection:
            self.connection = await connect(self.host)
        param = self.prefix + "." + param
        logging.info("Send: {} {}".format(param, value))
        await self.connection.send(param, value)

    def delay(self):
        return 20
