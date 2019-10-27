class WaterLevelMonitor:
    def __init__(self, level, graphite):
        self.level = level
        self.graphite = graphite

    def __call__(self):
        self.graphite.send("plants.waterlevel", self.level())

    def delay(self):
        return 20
