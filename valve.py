# Valve class:

class Valve:
    valve_type = None
    valve_name = None
    status = False 
    port = None

    # valve_type = ball, soleniod, etc
    # status = open or closed => open = True => closed = False
    # port = serial port

    # Setters:
    def __init__(self, valve_type, valve_name, status, port):
        self.valve_type = valve_type
        self.valve_name = valve_name

        if(status == "close"):
            self.status = False
        elif(status == "open"):
            self.status = True

        self.port = port
    
    def set_port(self, port):
        self.port = port
    
    def open(self):
        self.status = True
        # talk to micro controller

    def close(self):
        self.status = False
        # talk to micro controller

    # Getters:
    def get_status(self):
        return self.status
    
    def get_valve_name(self):
        return self.valve_name
    
    def get_type(self):
        return self.valve_type

