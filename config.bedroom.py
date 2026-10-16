is_mock = False
th_monitor = True
graphite_instance = "bedroom"
soils = 0
distance = False
pump = False
pump2 = False
lightness = []
i2c = 1
light = False
light_sun = False
curtain_sun = True
level = False
invert_level = False
rtl433 = False
ping = False
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
    PUMP_ACTIVE_TIME = 20
    PUMP_WAIT_TIME = 60 * 60
    PUMP_ITERATIONS = 30

class PUMP_PARAMETERS2(PUMP_PARAMETERS):
    pass
