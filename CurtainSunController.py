import datetime
import logging


class CurtainSunController:
    def __init__(self, curtain, sun, graphite):
        self.curtain = curtain
        self.sun = sun
        self.graphite = graphite
        self.last_down_date = None

    async def __call__(self):
        now = datetime.datetime.now()
        sunrise = self.sun.sunrise()
        down_time = sunrise - datetime.timedelta(minutes=30)
        sent = 0

        if down_time <= now < sunrise and self.last_down_date != now.date():
            await self.curtain.down()
            self.last_down_date = now.date()
            sent = 1
            logging.info("Curtain down command sent before sunrise at %s", sunrise)

        await self.graphite.send("curtain_sun", sent)

    def delay(self):
        return 120
