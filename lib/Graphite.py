import graphyte
import logging

class Graphite:
    def __init__(self, host):
        graphyte.init(host)

    async def send(self, param, value):
        logging.info("Send: {} {}".format(param, value))
        for i in range(3):
            graphyte.send(param, value)

    def delay(self):
        return 20