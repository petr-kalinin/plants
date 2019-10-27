class THMonitor:
    def __init__(self, sht20, graphite):
        self.sht20 = sht20
        self.graphite = graphite

    def __call__(self):
        t = self.sht20.temperature()
        rh = self.sht20.humidity()
        self.graphite.send('plants.temperature', t)
        self.graphite.send('plants.humidity', rh)
        print("SHT20 temperature is", t, "humidity", rh)

    def delay(self):
        return self.graphite.delay()
