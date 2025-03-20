is_mock = False
th_monitor = True
graphite_instance = 1
soils = 0
distance = True
pump = True
pump2 = True
lightness = []
i2c = 1
light = True
light_sun = False
level = True
invert_level = False
rtl433 = False
ping = True
heater = False
display = False
joystick = False
heater_t_max = 20
dacha_pump = False
graphite_attempts = 5
procmonitor = False

class PUMP_PARAMETERS:
    AFTER_WATER_DELAY = 24 * 60 * 60
    PUMP_INIT_TIME = 3
    PUMP_POST_INIT_TIME = 3
    PUMP_ACTIVE_TIME = 300
    PUMP_WAIT_TIME = 2 * 60 * 60
    PUMP_ITERATIONS = 1

class PUMP_PARAMETERS2:
    AFTER_WATER_DELAY = 60 * 60
    PUMP_INIT_TIME = 1
    PUMP_POST_INIT_TIME = 1
    PUMP_ACTIVE_TIME = 5 * 60
    PUMP_WAIT_TIME = 60 * 60
    PUMP_ITERATIONS = 1
    LAST_TIME_FILE = "pump_controller_last_time_2.txt"
    LOCK_FILE = "pump_controller_lock_2"
