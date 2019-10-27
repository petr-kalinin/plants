class PumpController:
    def __init__(self, level, pump, graphite):
        self.level = level
        self.pump = pump
        self.graphite = graphite

    def delay(self):
        return 20
