from aiographite import connect
from aiographite.protocol import PlaintextProtocol
import logging

class Graphite:
    def __init__(self, host):
        self.connection = None
        self.host = host

    async def send(self, param, value):
        if not self.connection:
            self.connection = await connect(self.host)
        logging.info("Send: {} {}".format(param, value))
        await self.connection.send(param, value)

    def delay(self):
        return 20
