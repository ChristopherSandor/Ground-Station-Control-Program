from valve import Valve

# Data class:

class Data:
    valves_list = []
    sensors_list = []

    def __init__ (self, valve_list, sensor_list):
        

    def shutDown_ALL(self):
        for valve in self.valves_list:
            valve.close()


