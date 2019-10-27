import time

IDLE = 0
PUMPING = 1

AFTER_WATER_DELAY = 2 * 24 * 60 * 60
MAX_PUMP_TIME = 2 * 60

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
                 return int(f.read())
        except FileNotFoundError:
            return 0

    def save_time(self):
        with open("pump_controller_last_time.txt", "w") as f:
            f.write(str(self.last_level_time))

    def __call__(self):
        self.graphite.send("plants.pump", 0 if self.state == IDLE else 1)
        if self.level() > 0:
            self.last_level_time = time.time()
            self.save_time()

        if self.state == IDLE:
            if time.time() > self.last_level_time + AFTER_WATER_DELAY:
                self.pump.start()
                self.pump_start_time = time.time()
                self.state = PUMPING
        else:
            if self.level() > 0 or time.time() > self.pump_start_time + MAX_PUMP_TIME:
                self.pump.stop()
                self.state = IDLE

    def delay(self):
        if self.state == IDLE:
            return self.graphite.delay()
        else:
            return 0
