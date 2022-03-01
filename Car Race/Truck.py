import Vehicle

class Truck(Vehicle.Vehicle):
    
    def __init__(self,wheels,engine, brand,color,vehicle_shape):
        super().__init__(wheels, engine, brand,color,vehicle_shape)
        self.wheels= wheels
        self.engine = engine
        self.brand = brand
        self.color = color
        self.vehicle_shape= vehicle_shape
    
    def connect_trailer():
        print("trailer connected")