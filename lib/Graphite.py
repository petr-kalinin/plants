from aiographite import connect
from aiographite.protocol import PlaintextProtocol
import logging

class Graphite:
    def __init__(self, host, prefix):
        self.connection = None
        self.host = host
        self.prefix = prefix

    async def send(self, param, value):
        param = self.prefix + "." + param
        for i in range(5):
            try:
                logging.info("Send: {} {} attempt {}".format(param, value, i))
                if not self.connection:
                    self.connection = await connect(self.host)
                await self.connection.send(param, value)
                break
            except:
                await asyncio.sleep((2 ** i) / 10)

    def delay(self):
        return 20
