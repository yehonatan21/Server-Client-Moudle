# from Car import Car
# from Bike import Bike
# from Truck import Truck

class Vehicle():

    def __init__(self,wheels: str,engein: int,brand:str, color, vehicle_shape):
        # assert engein >= 50, f"the {engein} is not valid. "
        assert wheels > 0, f"the {wheels} are not valid. "

        self.engientype = engein
        self.wheels = wheels
        self.brand = brand
        self.color = color
        self.vehicle_shape= vehicle_shape

    def shift_gear():
        pass

    def start_engien(self):     
        print ("Engine is on")
    
    def stop_engien(self):
        print ("Engine is off")

    def get_wheels(self):
        return self.many_wheels
    
    def get_Type (self):
        return self.type    

    def get_company (self):
        return self.brand
    
    def get_engine_size (self):
        return self.engine_size