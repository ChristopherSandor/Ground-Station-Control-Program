# Sensor class:
from collections import deque
import serial
import time

def is_within_tolerance(num, target, tol):
    verdict = (abs(num - target) < tol)
    return verdict

class Sensor:
    sensor_name = None
    port = None
    s_data = 0.0
    ser = None
    trend_collection = None

   # Setters:
    def __init__ (self, sensor_name, port):
        self.sensor_name = sensor_name
        self.port = port
        self.s_data = 0
        self.trend_collection = deque(maxlen=5)
        self.trend_collection.append(0)

        if(type(self).ser == None):
            type(self).ser = serial.Serial(port, 115200, timeout=1)

   # Getters:

    def translate_data(self, raw_data):
        # Do shit here from microcontroller and translate it to an actual number
        true_data = raw_data.decode('utf-8').strip()

        return float(true_data)

    def get_data(self):
        raw = type(self).ser.readline()
        self.s_data = self.translate_data(raw)
        return self.s_data


    def trend(self, tol=7.5):

        if len(self.trend_collection) < 2:
            return None

        first = self.trend_collection[0]
        last  = self.trend_collection[-1]
        delta = last - first

        if abs(delta) < tol:
            return None       # small change
        elif delta > 0:
            return True       # rising fast
        else:
            return False      # falling fast