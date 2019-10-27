import datetime

on_periods = ((datetime.time(6, 0), datetime.time(22, 0)),
              (datetime.time(6, 30), datetime.time(21, 30)),
              (datetime.time(7, 0), datetime.time(21, 0)))

class LightController:
    def __init__(self, setter):
        self.setter = setter

    def __call__(self):
        time = datetime.datetime.now().time()
        values = []
        print("time=", time)
        for i in range(3):
            values.append(time > on_periods[i][0] and time < on_periods[i][1])
            print("value for light {} is {}".format(i, values[-1]))
        self.setter.set(values)
