# from _typeshed import Self
from Car import Car
from Bike import Bike
from Truck import Truck
from Vehicle import *
import types
import random

engine_types = {1:"fuel", 2:"electric"}
vehicleTypes = {1:"car" ,2:"truck", 3:"bike"}
colors = {0:"red", 1:"blue", 2:"green", 3:"yellow", 4: "black", 5:"grey", 6:"brown", 7:"cyan", 8:"purple", 9:"pink"}
brand = {1: "BMW", 2:"mini", 3:"tesla"}
vehicle_shape = {1:"arrow", 2:"square", 3:"turtle", 4:"circle"}

class Factory():
    __vehicles = [] 
    def __test():
        racers = Factory.create_vehicles(5)

    def __create(vehicle):
        match vehicle.type:
            case "car":
                vehicle = Car(vehicle.wheels, vehicle.engine, vehicle.brand, vehicle.color,vehicle.vehicle_shape)
            case "truck":
                vehicle = Truck(vehicle.wheels, vehicle.engine, vehicle.brand, vehicle.color,vehicle.vehicle_shape)
            case "bike":
                vehicle = Bike(vehicle.wheels, vehicle.engine, vehicle.brand, vehicle.color,vehicle.vehicle_shape)
        return vehicle

    def __set_type():
        type = "None"
        while type not in range(1,4):
            try:
                type = int(input("what kind of Vehicle do you want to creat? plese select the number: \n(1)Car \n(2)Truck \n(3)Bike \n"))
            except ValueError: 
                pass

    def __set_engine():
        engine = None
        engine_types = {1:"fuel", 2:"electric"}
        while engine not in engine_types.values():
            ans = int(input("what is the the engein type?\n(1)fuel \n(2)electric\nplese select number.\n "))   
            try:
                engine = engine_types[ans]
            except:
                pass

    def create_vehicles(num):
        for i in range(0,num):
            order = Factory.__create_order(
                vehicleTypes[random.randint(1,3)],
                engine_types[random.randint(1,2)],
                random.randint(2,4),
                brand[random.randint(1,3)],
                colors[random.randint(0,9)],
                vehicle_shape[random.randint(1,4)]
            )
        
            Factory.__vehicles.append(Factory.__create(order))
        return Factory.__vehicles

    def __check_type(vehicles_list):
        for i in range(0,len(vehicles_list)):
            if isinstance(vehicles_list[i-1], Car):
                print(f"Car: {i+1}" )
            elif isinstance(vehicles_list[i-1], Truck):
                print(f"Truck: {i+1}")
            elif isinstance(vehicles_list[i-1], Bike):
                print(f"Bike: {i+1}")

    def __create_order(type=None,engine=None, wheels=None, brand=None,color=None, vehicle_shape = None):
        return types.SimpleNamespace(type=type, wheels = wheels, engine = engine, brand = brand, color = color, vehicle_shape=vehicle_shape)

#if __name__ == "__main__":
 #   if True:
  #      Factory.test()
   # else:
    #    Factory.main()  