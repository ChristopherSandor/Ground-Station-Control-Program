from valve import Valve
from sensor import Sensor

# Data class:

class Data:
    valves_list = []
    sensors_list = []

    def __init__ (self, valve_list_file, sensor_list_file):
        
        with open(valve_list_file, 'r') as file:
            for raw_line in file:
                line = raw_line.strip()
                components = line.split(":",3)
                # components = [valve_type, valve_name, status, port]
                # valve_type:valve_name:status:port
                v = Valve(components[0], components[1], components[2], components[3])
                self.valves_list.append(v)
        
        with open(sensor_list_file, 'r') as file:
            for raw_line in file:
                line = raw_line.strip()
                components = line.split(":", 1)
                # components = [sensor_name, port]
                # sensor_name:port
                s = Sensor(components[0], components[1])
                self.sensors_list.append(s)

    def shutDown_ALL(self):
        for valve in self.valves_list:
            valve.close()


