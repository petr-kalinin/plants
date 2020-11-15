import datetime
import logging
import math

SUMMER_STARTS = (12, 2)
SUMMER_ENDS = (31, 10)
WINTER_STARTS = (30, 11)
WINTER_ENDS = (13, 1)

SUMMER_HIGH = 23
SUMMER_LOW = 15
SUMMER_MIDDLE = (SUMMER_HIGH + SUMMER_LOW) / 2

WINTER_HIGH = 12
WINTER_LOW = 7
WINTER_MIDDLE = (WINTER_HIGH + WINTER_LOW) / 2

HIGH_HOUR = 15.5

DELTA = 1

FIX_TIME_STEP = datetime.timedelta(minutes = 15)

def get_date(date, now_date):
    return datetime.date(day=date[0], month=date[1], year=now_date.year)

def get_boundary_from_date(summer, winter, now_date):
    summer_starts = get_date(SUMMER_STARTS, now_date)
    summer_ends = get_date(SUMMER_ENDS, now_date)
    winter_starts = get_date(WINTER_STARTS, now_date)
    winter_ends = get_date(WINTER_ENDS, now_date)
    if now_date < winter_ends:
        return winter
    elif now_date < summer_starts:
        f = (now_date - winter_ends) / (summer_starts - winter_ends)
        return f * summer + (1 - f) * winter
    elif now_date < summer_ends:
        return summer
    elif now_date < winter_starts:
        f = (now_date - summer_ends) / (winter_starts - summer_ends)
        return f * winter + (1 - f) * summer
    else:
        return winter

def get_boundary(summer, winter):
    now_date = datetime.datetime.now().date()
    return get_boundary_from_date(summer, winter, now_date)

def get_high():
    return get_boundary(SUMMER_HIGH, WINTER_HIGH)

def get_middle():
    return get_boundary(SUMMER_MIDDLE, WINTER_MIDDLE)

def unscaled_target(phase):
    base = math.cos(phase)
    x = abs(base) ** (1/2)
    if base < 0:
        x = - x
    return x

class HeaterController:
    def __init__(self, heater, temperature, display, joystick, graphite):
        self.heater = heater
        self.temperature = temperature
        self.graphite = graphite
        self.display = display
        self.joystick = joystick
        self.fix_target = None
        self.fix_time = None
        self.started = [False, False]

    def raw_target(self):
        time = datetime.datetime.now().time()
        hour = time.hour + time.minute / 60
        return unscaled_target((hour - HIGH_HOUR) / 24 * 2 * math.pi) * (get_high() - get_middle()) + get_middle()

    def init_fix(self):
        if self.fix_time is None:
            self.fix_time = datetime.datetime.now() + FIX_TIME_STEP
        if self.fix_target is None:
            self.fix_target = self.raw_target()

    async def update_fix(self):
        if not self.joystick:
            return
        joystick = await self.joystick()
        if joystick[0] != 0:
            self.init_fix()
            self.fix_time += joystick[0] * FIX_TIME_STEP
        if joystick[1] != 0:
            self.init_fix()
            self.fix_target += joystick[1]
        if self.fix_time is not None and self.fix_time < datetime.datetime.now():
            self.fix_time = None
            self.fix_target = None

    def get_target(self):
        if self.fix_time:
            return self.fix_target
        return self.raw_target()

    async def __call__(self):
        await self.update_fix()
        temperature = await self.temperature.temperature()
        target = self.get_target()
        logging.info("Temperature for heater is {}".format(temperature))
        logging.info("Target temperature for heater is {}".format(target))
        if self.fix_time:
            logging.info("Fix target for heater is {}".format(self.fix_target))
            logging.info("Fix time for heater is {}".format(self.fix_time))
        # heater 1
        if temperature < target:
            logging.info("Starting heater 1")
            self.started[0] = True
        if temperature > target + DELTA:
            logging.info("Stopping heater 1")
            self.started[0] = False
        # heater 2
        if temperature < target - DELTA:
            logging.info("Starting heater 2")
            self.started[1] = True
        if temperature > target:
            logging.info("Stopping heater 2")
            self.started[1] = False
        for i in range(2):
            if self.started[i]:
                await self.heater.start(i)
            else:
                await self.heater.stop(i)
        if self.display:
            time = datetime.datetime.now().time()
            self.display.print("%02d:%02d"% (time.hour, time.minute), 0)
            if self.fix_target:
                fix_target_str = "FIX: %2.1f" % (self.fix_target)
            else:
                fix_target_str = ""
            if self.fix_time:
                fix_time_str = " to: %02d:%02d" % (self.fix_time.hour, self.fix_time.minute)
            else:
                fix_time_str = ""
            self.display.print("%s%s"% (fix_target_str, fix_time_str), 1)
            self.display.print("T=%2.1f -> %2.1f" % (temperature, self.raw_target()), 2)
            self.display.print(" / ".join(["ON" if self.started[i] else "off" for i in range(2)]), 3)
        for i in range(2):
            await self.graphite.send("heater.{}".format(i), 1 if self.started[i] else 0)
        await self.graphite.send("heater_target", target)

    def delay(self):
        return 1


if __name__ == "__main__":
    date = datetime.date(day=1, month=1, year=2020)
    while date.year <= 2021:
        print(date, get_boundary_from_date(SUMMER_LOW, WINTER_LOW, date), get_boundary_from_date(SUMMER_HIGH, WINTER_HIGH, date))
        date = date + datetime.timedelta(days=1)