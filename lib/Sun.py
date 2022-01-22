#!/usr/bin/python3
from astral import LocationInfo
import astral.sun
import datetime

city = LocationInfo("LondoNizhny Novgorod", "Russia", "Europe/Moscow", 56, 44)

class Sun:
    def sunset(self):
       return astral.sun.sun(city.observer, date=datetime.date.today(), tzinfo=city.timezone)["sunset"].replace(tzinfo=None)

    def daylength(self):
       s = astral.sun.sun(city.observer, date=datetime.date.today(), tzinfo=city.timezone)
       return s["sunset"] - s["sunrise"]

if __name__ == "__main__":
    s = Sun()
    print(s.sunset())
    print(datetime.datetime.now() - s.sunset())
    print(s.daylength())

