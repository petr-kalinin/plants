is_mock = False
th_monitor = False
graphite_instance = "alena"
soils = 0
distance = False
pump = False
lightness = []
i2c = 1
light = False
light_sun = False
level = False
invert_level = True
rtl433 = False
ping = True
heater = False
display = False
joystick = False
heater_t_max = 20
dacha_pump = False
graphite_attempts = 5

class PUMP_PARAMETERS:
    AFTER_WATER_DELAY = 1 * 24 * 60 * 60
    PUMP_INIT_TIME = 3
    PUMP_POST_INIT_TIME = 3
    PUMP_ACTIVE_TIME = 20
    PUMP_WAIT_TIME = 60 * 60
    PUMP_ITERATIONS = 30
