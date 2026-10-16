import datetime
import logging


class CurtainSunController:
    def __init__(self, curtain, sun, graphite):
        self.curtain = curtain
        self.sun = sun
        self.graphite = graphite
        self.attempt_date = None
        self.attempts = 0

    async def __call__(self):
        now = datetime.datetime.now()
        sunrise = self.sun.sunrise()
        down_time = sunrise - datetime.timedelta(minutes=30)
        sent = 0

        if self.attempt_date != now.date():
            self.attempt_date = now.date()
            self.attempts = 0

        if self.attempts < 5 and (down_time <= now < sunrise or self.attempts > 0):
            self.attempts += 1
            await self.curtain.down()
            sent = 1
            logging.info("Curtain down attempt %d/5 for sunrise at %s", self.attempts, sunrise)

        await self.graphite.send("curtain_sun", sent)

    def delay(self):
        return 120
