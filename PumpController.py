import asyncio
import os
import time
import logging

from config import PUMP_PARAMETERS as P

class PumpController:
    def __init__(self, level, pump, graphite):
        self.level = level
        self.pump = pump
        self.graphite = graphite
        self.last_level_time = self.load_time()
        self.pump_start_time = None

    def load_time(self):
        try:
            with open("pump_controller_last_time.txt") as f:
                 return float(f.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_time(self):
        with open("pump_controller_last_time.txt", "w") as f:
            f.write(str(self.last_level_time))

    async def __call__(self):
        if os.path.exists("pump_controller_lock"):
            await self.graphite.send("pump", -1)
            return
        await self.graphite.send("pump", 0)

        if await self.level() > 0:
            self.last_level_time = time.time()
            self.save_time()

        if time.time() > self.last_level_time + P.AFTER_WATER_DELAY:
            await self.run_pump()
        else:
            await self.pump.stop()
            
    async def run_pump(self):
        try:
            for i in range(P.PUMP_ITERATIONS):
                if await self.level() > 0:
                    break
                await self.pump.start()
                await asyncio.sleep(P.PUMP_INIT_TIME)
                await self.pump.stop()
                await asyncio.sleep(P.PUMP_POST_INIT_TIME)
                await self.pump.start()
                start_time = time.time()
                while await self.level() == 0 and time.time() < start_time + P.PUMP_ACTIVE_TIME:
                    await self.graphite.send("pump", 1)
                    await asyncio.sleep(1)
                await self.pump.stop()
                # make sure pump=1 makes it to Graphite
                for i in range(4):
                    await self.graphite.send("pump", 1)
                    await asyncio.sleep(20)
                start_time = time.time()
                while time.time() < start_time + P.PUMP_WAIT_TIME:
                    await self.pump.stop()
                    await self.graphite.send("pump", 0)
                    await asyncio.sleep(10)
        finally:
            await self.pump.stop()
        self.last_level_time = time.time()
        self.save_time()

    def delay(self):
        return self.graphite.delay()
