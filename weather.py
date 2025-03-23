class BarometerBaseline:
    def __init__(self, pressure, timestamp):
        self._pressure = pressure
        self._timestamp = timestamp

    def get_pressure(self):
        return self._pressure

    def set_pressure(self, value):
        self._pressure = value

    def get_timestamp(self):
        return self._timestamp

    def set_timestamp(self, value):
        self._timestamp = value
