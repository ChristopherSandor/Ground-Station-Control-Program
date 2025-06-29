# Sensor class:

class Sensor:
    sensor_name = None
    port = None
    s_data = None
    

   # Setters:
    def __init__ (self, sensor_name, port):
        self.sensor_name = sensor_name
        self.s_data = 0
        self.port = port
    
    def set_port(self, port):
        self.port = port
    
   # Getters:
    def get_data(self):
        self.s_data = self.translate_data()
        return self.s_data
    
    def translate_data(self):
        # Do shit here from microcontroller and translate it to an actual number
        return None
