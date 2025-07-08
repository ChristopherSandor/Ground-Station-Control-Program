# Sensor class:
from collections import deque

def is_within_tolerance(num, target, tol):
    verdict = (abs(num - target) < tol)
    return verdict

class Sensor:
    sensor_name = None
    port = None
    s_data = 0.0

    # Count is helper for rn delete later
    count = 0
    trigger = True

    trend_collection = None

   # Setters:
    def __init__ (self, sensor_name, port):
        self.sensor_name = sensor_name
        self.s_data = 0
        self.port = port
        self.trend_collection = deque(maxlen=5)
        self.trend_collection.append(0)
        self.trigger = True
    
    def set_port(self, port):
        self.port = port
    
   # Getters:
    def get_data(self):

        # Gets New Data:
        if(self.count > 100 and self.trigger == False):
            self.count = self.count - 8
            self.trigger = True
        else:
            self.count = self.count + 1
            
        self.s_data = self.count

        # Updates New Trend
        self.trend_collection.append(self.s_data)

        return self.s_data

    def translate_data(self):
        # Do shit here from microcontroller and translate it to an actual number
        return None

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