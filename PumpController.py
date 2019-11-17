import os
import time
import logging

from is_mock import is_mock

IDLE = 0
PUMPING = 1

if is_mock:
    AFTER_WATER_DELAY = 60
    MAX_PUMP_TIME = 5
else:
    AFTER_WATER_DELAY = 3 * 24 * 60 * 60
    MAX_PUMP_TIME = 15 * 60


class PumpController:
    def __init__(self, level, pump, graphite):
        self.level = level
        self.pump = pump
        self.graphite = graphite
        self.state = IDLE
        self.last_level_time = self.load_time()
        self.pump_start_time = None

    def load_time(self):
        try:
            with open("pump_controller_last_time.txt") as f:
                 return float(f.read())
        except FileNotFoundError:
            return 0

    def save_time(self):
        with open("pump_controller_last_time.txt", "w") as f:
            f.write(str(self.last_level_time))

    async def __call__(self):
        if os.path.exists("pump_controller_lock"):
            await self.graphite.send("plants.pump", -1)
            return
        await self.graphite.send("plants.pump", 0 if self.state == IDLE else 1)
        if await self.level() > 0 or self.state == PUMPING:
            self.last_level_time = time.time()
            self.save_time()

        if self.state == IDLE:
            if time.time() > self.last_level_time + AFTER_WATER_DELAY:
                self.pump_start_time = time.time()
                self.state = PUMPING
        else:
            if await self.level() > 0 or time.time() > self.pump_start_time + MAX_PUMP_TIME:
                self.state = IDLE

        if self.state == IDLE:
            await self.pump.stop()
        else:
            await self.pump.start()


    def delay(self):
        if self.state == IDLE:
            return self.graphite.delay()
        else:
            return 0
